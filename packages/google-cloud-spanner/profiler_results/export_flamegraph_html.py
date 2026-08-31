"""Converts Python cProfile / .prof files into standalone interactive HTML Flame Graphs.

Fixes:
- Uses global flamegraph() constructor with fallback and graceful error messaging
- Dynamically resolves working directory
- Lightweight JSON payload (~100-300 KB) for instant browser rendering
- Zero external pip dependencies required
"""

import io
import json
import os
import pstats
import sys


def pstats_to_tree(pstats_file):
    """Parses a pstats file and converts it into a hierarchical flame graph tree JSON."""
    ps = pstats.Stats(pstats_file)
    ps.strip_dirs()

    all_funcs = ps.stats

    # Build caller -> callee map
    callees_map = {}

    for func, (cc, nc, tt, ct, callers) in all_funcs.items():
        func_name = f"{func[0]}:{func[1]}({func[2]})"
        for caller_func, caller_info in callers.items():
            if isinstance(caller_func, tuple):
                c_name = f"{caller_func[0]}:{caller_func[1]}({caller_func[2]})"
            else:
                c_name = str(caller_func)
            if c_name not in callees_map:
                callees_map[c_name] = []
            callees_map[c_name].append((func, ct, tt, cc))

    # Sort callees by cumulative time
    for c_name in callees_map:
        callees_map[c_name].sort(key=lambda x: x[1], reverse=True)

    sorted_funcs = sorted(all_funcs.items(), key=lambda x: x[1][3], reverse=True)
    total_time = ps.total_tt
    min_cutoff = max(0.05, total_time * 0.008)

    def build_node(func_tuple, visited, current_depth=0, max_depth=8):
        file_name, line_no, func_name = func_tuple
        node_id = f"{file_name}:{line_no}({func_name})"
        cc, nc, tt, ct, callers = all_funcs.get(func_tuple, (1, 1, 0, 0, {}))

        children = []
        if current_depth < max_depth and node_id in callees_map and node_id not in visited:
            visited_next = visited | {node_id}
            for child_tuple, child_ct, child_tt, child_cc in callees_map[node_id][:5]:
                if child_ct >= min_cutoff and child_tuple != func_tuple:
                    child_node = build_node(child_tuple, visited_next, current_depth + 1, max_depth)
                    if child_node["value"] > 0:
                        children.append(child_node)

        return {
            "name": f"{func_name} [{file_name}:{line_no}]",
            "value": round(ct, 4),
            "self_time": round(tt, 4),
            "calls": cc,
            "children": children,
        }

    # Find root entry points
    top_entries = []
    for func_tuple, (cc, nc, tt, ct, callers) in sorted_funcs:
        file_name = func_tuple[0]
        if any(p in file_name for p in ["spanner_cpu_profile_suite", "run_point_select", "run_limit_1000", "runners.py", "app.py"]):
            top_entries.append(func_tuple)
            if len(top_entries) >= 3:
                break

    if not top_entries and sorted_funcs:
        top_entries = [sorted_funcs[0][0]]

    root_children = [build_node(t, set(), 1) for t in top_entries]

    root = {
        "name": f"Total Profiled Workload ({total_time:.3f}s)",
        "value": round(total_time, 4),
        "self_time": 0.0,
        "calls": 1,
        "children": root_children,
    }
    return root, total_time, ps


def generate_flamegraph_html(prof_path, html_path, title):
    """Generates a standalone, fully interactive HTML flame graph with D3-flame-graph."""
    tree_data, total_time, ps = pstats_to_tree(prof_path)

    s = io.StringIO()
    ps.stream = s
    ps.sort_stats("cumulative").print_stats(20)
    top_table_text = s.getvalue()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title} - CPU Flame Graph</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/d3-flame-graph@4.1.3/dist/d3-flamegraph.css">
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 24px;
      background: #f8f9fa;
      color: #202124;
    }}
    .header {{
      background: #ffffff;
      padding: 20px 24px;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      margin-bottom: 20px;
    }}
    h1 {{
      margin: 0 0 8px 0;
      font-size: 24px;
      color: #1a73e8;
    }}
    .meta {{
      font-size: 14px;
      color: #5f6368;
    }}
    .card {{
      background: #ffffff;
      padding: 24px;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      margin-bottom: 24px;
    }}
    .controls {{
      margin-bottom: 16px;
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    input[type="text"] {{
      padding: 8px 12px;
      border: 1px solid #dadce0;
      border-radius: 4px;
      font-size: 14px;
      width: 280px;
    }}
    button {{
      padding: 8px 16px;
      background: #1a73e8;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
    }}
    button:hover {{
      background: #1557b0;
    }}
    button.secondary {{
      background: #f1f3f4;
      color: #3c4043;
    }}
    button.secondary:hover {{
      background: #e8eaed;
    }}
    #details {{
      margin-top: 12px;
      font-size: 14px;
      font-weight: 500;
      color: #1a73e8;
      min-height: 20px;
    }}
    #chart {{
      width: 100%;
      min-height: 500px;
    }}
    pre {{
      background: #202124;
      color: #e8eaed;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
      font-size: 13px;
      line-height: 1.4;
    }}
    .error-box {{
      display: none;
      padding: 12px 16px;
      background: #fce8e6;
      color: #c5221f;
      border-radius: 4px;
      margin-bottom: 12px;
      font-size: 14px;
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1>{title}</h1>
    <div class="meta">
      <strong>Source Profile:</strong> <code>{os.path.basename(prof_path)}</code> |
      <strong>Total Profiled CPU Time:</strong> {total_time:.4f} seconds |
      <strong>Interactive:</strong> Click any frame to zoom in, click root or 'Reset Zoom' to zoom out.
    </div>
  </div>

  <div class="card">
    <div class="controls">
      <input type="text" id="search" placeholder="Search function or module...">
      <button onclick="search()">Search</button>
      <button class="secondary" onclick="clearSearch()">Clear</button>
      <button class="secondary" onclick="resetZoom()">Reset Zoom</button>
    </div>
    <div id="error-box" class="error-box"></div>
    <div id="details">Hover over a function to view time and call metrics</div>
    <div id="chart"></div>
  </div>

  <div class="card">
    <h2>Top 20 Functions by Cumulative CPU Time</h2>
    <pre>{top_table_text}</pre>
  </div>

  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/d3-flame-graph@4.1.3/dist/d3-flamegraph.min.js"></script>
  <script>
    const data = {json.dumps(tree_data)};

    let flamegraphInstance = null;

    try {{
      // Correct constructor resolution: global flamegraph() or d3.flamegraph()
      const createFlamegraph = (typeof flamegraph === 'function') 
        ? flamegraph 
        : (typeof d3 !== 'undefined' && typeof d3.flamegraph === 'function' ? d3.flamegraph : null);

      if (!createFlamegraph) {{
        throw new Error("Flamegraph library failed to load. Please check internet access for CDN scripts.");
      }}

      flamegraphInstance = createFlamegraph()
        .width(document.getElementById('chart').offsetWidth || 1100)
        .cellHeight(20)
        .transitionDuration(400)
        .minFrameSize(2)
        .transitionEase(d3.easeCubic)
        .sort(true)
        .title("")
        .onClick(function (d) {{
          console.info("Clicked on " + d.data.name);
        }})
        .setDetailsElement(document.getElementById("details"));

      d3.select("#chart")
        .datum(data)
        .call(flamegraphInstance);

      window.addEventListener('resize', () => {{
        if (flamegraphInstance) {{
          flamegraphInstance.width(document.getElementById('chart').offsetWidth);
          d3.select("#chart").call(flamegraphInstance);
        }}
      }});
    }} catch (err) {{
      console.error("Error initializing flamegraph:", err);
      const errBox = document.getElementById("error-box");
      errBox.style.display = "block";
      errBox.textContent = "Error rendering flame graph: " + err.message;
    }}

    function search() {{
      const term = document.getElementById("search").value;
      if (term && flamegraphInstance) {{
        flamegraphInstance.search(term);
      }}
    }}

    function clearSearch() {{
      document.getElementById("search").value = "";
      if (flamegraphInstance) {{
        flamegraphInstance.clear();
      }}
    }}

    function resetZoom() {{
      if (flamegraphInstance) {{
        flamegraphInstance.resetZoom();
      }}
    }}
  </script>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] Generated Interactive Flame Graph HTML: {html_path}")


def main():
    profile_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()

    scenarios = [
        ("spanner_point_select_c1.prof", "spanner_point_select_c1.html", "Scenario 1: Point Select (Concurrency = 1) - Real Spanner"),
        ("spanner_point_select_c32.prof", "spanner_point_select_c32.html", "Scenario 2: Point Select (Concurrency = 32 Coroutines) - Real Spanner"),
        ("spanner_limit1000_c1.prof", "spanner_limit1000_c1.html", "Scenario 3: LIMIT 1000 Read (11 Columns) - Real Spanner"),
        ("spanner_point_select_c32_threads.prof", "spanner_point_select_c32_threads.html", "Scenario 4: Point Select Multi-Threaded (C=32 Threads) - Real Spanner & GIL Contention"),
        ("spanner_point_select_c32_multiprocess.prof", "spanner_point_select_c32_multiprocess.html", "Scenario 5: Multi-Processing (4 Procs x 8 Threads = 32 Concurrency) - Real Spanner"),
    ]

    for prof_name, html_name, title in scenarios:
        prof_p = os.path.join(profile_dir, prof_name)
        html_p = os.path.join(profile_dir, html_name)
        if os.path.exists(prof_p):
            generate_flamegraph_html(prof_p, html_p, title)
        else:
            print(f"[-] Profile file not found: {prof_p}")


if __name__ == "__main__":
    main()
