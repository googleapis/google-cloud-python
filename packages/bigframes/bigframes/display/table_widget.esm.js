var __defProp = Object.defineProperty;
var __markAsModule = (target) => __defProp(target, "__esModule", { value: true });
var __require = typeof require !== "undefined" ? require : (x2) => {
  throw new Error('Dynamic require of "' + x2 + '" is not supported');
};
var __export = (target, all) => {
  __markAsModule(target);
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};

// bigframes/display/react.js
var react_exports = {};
__export(react_exports, {
  Children: () => fe,
  Component: () => le,
  Fragment: () => ae,
  Profiler: () => pe,
  PureComponent: () => ye,
  StrictMode: () => de,
  Suspense: () => _e,
  __SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED: () => me,
  cloneElement: () => he,
  createContext: () => ve,
  createElement: () => Se,
  createFactory: () => Ee,
  createRef: () => Re,
  default: () => Be,
  forwardRef: () => Ce,
  isValidElement: () => ke,
  lazy: () => we,
  memo: () => be,
  startTransition: () => $e,
  unstable_act: () => je,
  useCallback: () => xe,
  useContext: () => Oe,
  useDebugValue: () => Ie,
  useDeferredValue: () => ge,
  useEffect: () => Pe,
  useId: () => Te,
  useImperativeHandle: () => De,
  useInsertionEffect: () => Ve,
  useLayoutEffect: () => Le,
  useMemo: () => Ne,
  useReducer: () => Fe,
  useRef: () => Ue,
  useState: () => qe,
  useSyncExternalStore: () => Ae,
  useTransition: () => Me,
  version: () => ze
});
var F = Object.create;
var k = Object.defineProperty;
var U = Object.getOwnPropertyDescriptor;
var q = Object.getOwnPropertyNames;
var A = Object.getPrototypeOf;
var M = Object.prototype.hasOwnProperty;
var w = (e2, t) => () => (t || e2((t = { exports: {} }).exports, t), t.exports);
var z = (e2, t, r, u) => {
  if (t && typeof t == "object" || typeof t == "function")
    for (let o of q(t))
      !M.call(e2, o) && o !== r && k(e2, o, { get: () => t[o], enumerable: !(u = U(t, o)) || u.enumerable });
  return e2;
};
var B = (e2, t, r) => (r = e2 != null ? F(A(e2)) : {}, z(t || !e2 || !e2.__esModule ? k(r, "default", { value: e2, enumerable: true }) : r, e2));
var V = w((n) => {
  "use strict";
  var y = Symbol.for("react.element"), H = Symbol.for("react.portal"), W = Symbol.for("react.fragment"), Y = Symbol.for("react.strict_mode"), G = Symbol.for("react.profiler"), J = Symbol.for("react.provider"), K2 = Symbol.for("react.context"), Q = Symbol.for("react.forward_ref"), X2 = Symbol.for("react.suspense"), Z2 = Symbol.for("react.memo"), ee2 = Symbol.for("react.lazy"), b = Symbol.iterator;
  function te(e2) {
    return e2 === null || typeof e2 != "object" ? null : (e2 = b && e2[b] || e2["@@iterator"], typeof e2 == "function" ? e2 : null);
  }
  var x2 = { isMounted: function() {
    return false;
  }, enqueueForceUpdate: function() {
  }, enqueueReplaceState: function() {
  }, enqueueSetState: function() {
  } }, O = Object.assign, I = {};
  function p(e2, t, r) {
    this.props = e2, this.context = t, this.refs = I, this.updater = r || x2;
  }
  p.prototype.isReactComponent = {};
  p.prototype.setState = function(e2, t) {
    if (typeof e2 != "object" && typeof e2 != "function" && e2 != null)
      throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
    this.updater.enqueueSetState(this, e2, t, "setState");
  };
  p.prototype.forceUpdate = function(e2) {
    this.updater.enqueueForceUpdate(this, e2, "forceUpdate");
  };
  function g() {
  }
  g.prototype = p.prototype;
  function S2(e2, t, r) {
    this.props = e2, this.context = t, this.refs = I, this.updater = r || x2;
  }
  var E = S2.prototype = new g();
  E.constructor = S2;
  O(E, p.prototype);
  E.isPureReactComponent = true;
  var $2 = Array.isArray, P = Object.prototype.hasOwnProperty, R = { current: null }, T = { key: true, ref: true, __self: true, __source: true };
  function D2(e2, t, r) {
    var u, o = {}, c = null, f = null;
    if (t != null)
      for (u in t.ref !== void 0 && (f = t.ref), t.key !== void 0 && (c = "" + t.key), t)
        P.call(t, u) && !T.hasOwnProperty(u) && (o[u] = t[u]);
    var i = arguments.length - 2;
    if (i === 1)
      o.children = r;
    else if (1 < i) {
      for (var s = Array(i), a = 0; a < i; a++)
        s[a] = arguments[a + 2];
      o.children = s;
    }
    if (e2 && e2.defaultProps)
      for (u in i = e2.defaultProps, i)
        o[u] === void 0 && (o[u] = i[u]);
    return { $$typeof: y, type: e2, key: c, ref: f, props: o, _owner: R.current };
  }
  function re(e2, t) {
    return { $$typeof: y, type: e2.type, key: t, ref: e2.ref, props: e2.props, _owner: e2._owner };
  }
  function C(e2) {
    return typeof e2 == "object" && e2 !== null && e2.$$typeof === y;
  }
  function ne2(e2) {
    var t = { "=": "=0", ":": "=2" };
    return "$" + e2.replace(/[=:]/g, function(r) {
      return t[r];
    });
  }
  var j = /\/+/g;
  function v(e2, t) {
    return typeof e2 == "object" && e2 !== null && e2.key != null ? ne2("" + e2.key) : t.toString(36);
  }
  function _(e2, t, r, u, o) {
    var c = typeof e2;
    (c === "undefined" || c === "boolean") && (e2 = null);
    var f = false;
    if (e2 === null)
      f = true;
    else
      switch (c) {
        case "string":
        case "number":
          f = true;
          break;
        case "object":
          switch (e2.$$typeof) {
            case y:
            case H:
              f = true;
          }
      }
    if (f)
      return f = e2, o = o(f), e2 = u === "" ? "." + v(f, 0) : u, $2(o) ? (r = "", e2 != null && (r = e2.replace(j, "$&/") + "/"), _(o, t, r, "", function(a) {
        return a;
      })) : o != null && (C(o) && (o = re(o, r + (!o.key || f && f.key === o.key ? "" : ("" + o.key).replace(j, "$&/") + "/") + e2)), t.push(o)), 1;
    if (f = 0, u = u === "" ? "." : u + ":", $2(e2))
      for (var i = 0; i < e2.length; i++) {
        c = e2[i];
        var s = u + v(c, i);
        f += _(c, t, r, s, o);
      }
    else if (s = te(e2), typeof s == "function")
      for (e2 = s.call(e2), i = 0; !(c = e2.next()).done; )
        c = c.value, s = u + v(c, i++), f += _(c, t, r, s, o);
    else if (c === "object")
      throw t = String(e2), Error("Objects are not valid as a React child (found: " + (t === "[object Object]" ? "object with keys {" + Object.keys(e2).join(", ") + "}" : t) + "). If you meant to render a collection of children, use an array instead.");
    return f;
  }
  function d(e2, t, r) {
    if (e2 == null)
      return e2;
    var u = [], o = 0;
    return _(e2, u, "", "", function(c) {
      return t.call(r, c, o++);
    }), u;
  }
  function oe2(e2) {
    if (e2._status === -1) {
      var t = e2._result;
      t = t(), t.then(function(r) {
        (e2._status === 0 || e2._status === -1) && (e2._status = 1, e2._result = r);
      }, function(r) {
        (e2._status === 0 || e2._status === -1) && (e2._status = 2, e2._result = r);
      }), e2._status === -1 && (e2._status = 0, e2._result = t);
    }
    if (e2._status === 1)
      return e2._result.default;
    throw e2._result;
  }
  var l = { current: null }, m = { transition: null }, ue2 = { ReactCurrentDispatcher: l, ReactCurrentBatchConfig: m, ReactCurrentOwner: R };
  n.Children = { map: d, forEach: function(e2, t, r) {
    d(e2, function() {
      t.apply(this, arguments);
    }, r);
  }, count: function(e2) {
    var t = 0;
    return d(e2, function() {
      t++;
    }), t;
  }, toArray: function(e2) {
    return d(e2, function(t) {
      return t;
    }) || [];
  }, only: function(e2) {
    if (!C(e2))
      throw Error("React.Children.only expected to receive a single React element child.");
    return e2;
  } };
  n.Component = p;
  n.Fragment = W;
  n.Profiler = G;
  n.PureComponent = S2;
  n.StrictMode = Y;
  n.Suspense = X2;
  n.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = ue2;
  n.cloneElement = function(e2, t, r) {
    if (e2 == null)
      throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e2 + ".");
    var u = O({}, e2.props), o = e2.key, c = e2.ref, f = e2._owner;
    if (t != null) {
      if (t.ref !== void 0 && (c = t.ref, f = R.current), t.key !== void 0 && (o = "" + t.key), e2.type && e2.type.defaultProps)
        var i = e2.type.defaultProps;
      for (s in t)
        P.call(t, s) && !T.hasOwnProperty(s) && (u[s] = t[s] === void 0 && i !== void 0 ? i[s] : t[s]);
    }
    var s = arguments.length - 2;
    if (s === 1)
      u.children = r;
    else if (1 < s) {
      i = Array(s);
      for (var a = 0; a < s; a++)
        i[a] = arguments[a + 2];
      u.children = i;
    }
    return { $$typeof: y, type: e2.type, key: o, ref: c, props: u, _owner: f };
  };
  n.createContext = function(e2) {
    return e2 = { $$typeof: K2, _currentValue: e2, _currentValue2: e2, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e2.Provider = { $$typeof: J, _context: e2 }, e2.Consumer = e2;
  };
  n.createElement = D2;
  n.createFactory = function(e2) {
    var t = D2.bind(null, e2);
    return t.type = e2, t;
  };
  n.createRef = function() {
    return { current: null };
  };
  n.forwardRef = function(e2) {
    return { $$typeof: Q, render: e2 };
  };
  n.isValidElement = C;
  n.lazy = function(e2) {
    return { $$typeof: ee2, _payload: { _status: -1, _result: e2 }, _init: oe2 };
  };
  n.memo = function(e2, t) {
    return { $$typeof: Z2, type: e2, compare: t === void 0 ? null : t };
  };
  n.startTransition = function(e2) {
    var t = m.transition;
    m.transition = {};
    try {
      e2();
    } finally {
      m.transition = t;
    }
  };
  n.unstable_act = function() {
    throw Error("act(...) is not supported in production builds of React.");
  };
  n.useCallback = function(e2, t) {
    return l.current.useCallback(e2, t);
  };
  n.useContext = function(e2) {
    return l.current.useContext(e2);
  };
  n.useDebugValue = function() {
  };
  n.useDeferredValue = function(e2) {
    return l.current.useDeferredValue(e2);
  };
  n.useEffect = function(e2, t) {
    return l.current.useEffect(e2, t);
  };
  n.useId = function() {
    return l.current.useId();
  };
  n.useImperativeHandle = function(e2, t, r) {
    return l.current.useImperativeHandle(e2, t, r);
  };
  n.useInsertionEffect = function(e2, t) {
    return l.current.useInsertionEffect(e2, t);
  };
  n.useLayoutEffect = function(e2, t) {
    return l.current.useLayoutEffect(e2, t);
  };
  n.useMemo = function(e2, t) {
    return l.current.useMemo(e2, t);
  };
  n.useReducer = function(e2, t, r) {
    return l.current.useReducer(e2, t, r);
  };
  n.useRef = function(e2) {
    return l.current.useRef(e2);
  };
  n.useState = function(e2) {
    return l.current.useState(e2);
  };
  n.useSyncExternalStore = function(e2, t, r) {
    return l.current.useSyncExternalStore(e2, t, r);
  };
  n.useTransition = function() {
    return l.current.useTransition();
  };
  n.version = "18.2.0";
});
var N = w((ie, L) => {
  "use strict";
  L.exports = V();
});
var h = B(N());
var { Children: fe, Component: le, Fragment: ae, Profiler: pe, PureComponent: ye, StrictMode: de, Suspense: _e, __SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED: me, cloneElement: he, createContext: ve, createElement: Se, createFactory: Ee, createRef: Re, forwardRef: Ce, isValidElement: ke, lazy: we, memo: be, startTransition: $e, unstable_act: je, useCallback: xe, useContext: Oe, useDebugValue: Ie, useDeferredValue: ge, useEffect: Pe, useId: Te, useImperativeHandle: De, useInsertionEffect: Ve, useLayoutEffect: Le, useMemo: Ne, useReducer: Fe, useRef: Ue, useState: qe, useSyncExternalStore: Ae, useTransition: Me, version: ze } = h;
var Be = h.default ?? h;

// bigframes/display/scheduler.js
var scheduler_exports = {};
__export(scheduler_exports, {
  default: () => Ie2,
  unstable_IdlePriority: () => ae2,
  unstable_ImmediatePriority: () => oe,
  unstable_LowPriority: () => se,
  unstable_NormalPriority: () => ce,
  unstable_Profiling: () => fe2,
  unstable_UserBlockingPriority: () => be2,
  unstable_cancelCallback: () => _e2,
  unstable_continueExecution: () => pe2,
  unstable_forceFrameRate: () => ve2,
  unstable_getCurrentPriorityLevel: () => de2,
  unstable_getFirstCallbackNode: () => ye2,
  unstable_next: () => me2,
  unstable_now: () => ue,
  unstable_pauseExecution: () => ge2,
  unstable_requestPaint: () => he2,
  unstable_runWithPriority: () => ke2,
  unstable_scheduleCallback: () => Pe2,
  unstable_shouldYield: () => we2,
  unstable_wrapCallback: () => xe2
});
var __setImmediate$ = (cb, ...args) => ({ $t: setTimeout(cb, 0, ...args), [Symbol.dispose]() {
  clearTimeout(this.t);
} });
var V2 = Object.create;
var B2 = Object.defineProperty;
var U2 = Object.getOwnPropertyDescriptor;
var X = Object.getOwnPropertyNames;
var Z = Object.getPrototypeOf;
var $ = Object.prototype.hasOwnProperty;
var D = (e2, n) => () => (n || e2((n = { exports: {} }).exports, n), n.exports);
var ee = (e2, n, t, l) => {
  if (n && typeof n == "object" || typeof n == "function")
    for (let i of X(n))
      !$.call(e2, i) && i !== t && B2(e2, i, { get: () => n[i], enumerable: !(l = U2(n, i)) || l.enumerable });
  return e2;
};
var ne = (e2, n, t) => (t = e2 != null ? V2(Z(e2)) : {}, ee(n || !e2 || !e2.__esModule ? B2(t, "default", { value: e2, enumerable: true }) : t, e2));
var K = D((r) => {
  "use strict";
  function L(e2, n) {
    var t = e2.length;
    e2.push(n);
    e:
      for (; 0 < t; ) {
        var l = t - 1 >>> 1, i = e2[l];
        if (0 < g(i, n))
          e2[l] = n, e2[t] = i, t = l;
        else
          break e;
      }
  }
  function o(e2) {
    return e2.length === 0 ? null : e2[0];
  }
  function k2(e2) {
    if (e2.length === 0)
      return null;
    var n = e2[0], t = e2.pop();
    if (t !== n) {
      e2[0] = t;
      e:
        for (var l = 0, i = e2.length, y = i >>> 1; l < y; ) {
          var f = 2 * (l + 1) - 1, I = e2[f], b = f + 1, m = e2[b];
          if (0 > g(I, t))
            b < i && 0 > g(m, I) ? (e2[l] = m, e2[b] = t, l = b) : (e2[l] = I, e2[f] = t, l = f);
          else if (b < i && 0 > g(m, t))
            e2[l] = m, e2[b] = t, l = b;
          else
            break e;
        }
    }
    return n;
  }
  function g(e2, n) {
    var t = e2.sortIndex - n.sortIndex;
    return t !== 0 ? t : e2.id - n.id;
  }
  typeof performance == "object" && typeof performance.now == "function" ? (q2 = performance, r.unstable_now = function() {
    return q2.now();
  }) : (C = Date, O = C.now(), r.unstable_now = function() {
    return C.now() - O;
  });
  var q2, C, O, s = [], c = [], te = 1, a = null, u = 3, P = false, _ = false, v = false, z2 = typeof setTimeout == "function" ? setTimeout : null, A2 = typeof clearTimeout == "function" ? clearTimeout : null, W = typeof __setImmediate$ < "u" ? __setImmediate$ : null;
  typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
  function N2(e2) {
    for (var n = o(c); n !== null; ) {
      if (n.callback === null)
        k2(c);
      else if (n.startTime <= e2)
        k2(c), n.sortIndex = n.expirationTime, L(s, n);
      else
        break;
      n = o(c);
    }
  }
  function j(e2) {
    if (v = false, N2(e2), !_)
      if (o(s) !== null)
        _ = true, M2(F2);
      else {
        var n = o(c);
        n !== null && R(j, n.startTime - e2);
      }
  }
  function F2(e2, n) {
    _ = false, v && (v = false, A2(d), d = -1), P = true;
    var t = u;
    try {
      for (N2(n), a = o(s); a !== null && (!(a.expirationTime > n) || e2 && !J()); ) {
        var l = a.callback;
        if (typeof l == "function") {
          a.callback = null, u = a.priorityLevel;
          var i = l(a.expirationTime <= n);
          n = r.unstable_now(), typeof i == "function" ? a.callback = i : a === o(s) && k2(s), N2(n);
        } else
          k2(s);
        a = o(s);
      }
      if (a !== null)
        var y = true;
      else {
        var f = o(c);
        f !== null && R(j, f.startTime - n), y = false;
      }
      return y;
    } finally {
      a = null, u = t, P = false;
    }
  }
  var w2 = false, h2 = null, d = -1, G = 5, H = -1;
  function J() {
    return !(r.unstable_now() - H < G);
  }
  function E() {
    if (h2 !== null) {
      var e2 = r.unstable_now();
      H = e2;
      var n = true;
      try {
        n = h2(true, e2);
      } finally {
        n ? p() : (w2 = false, h2 = null);
      }
    } else
      w2 = false;
  }
  var p;
  typeof W == "function" ? p = function() {
    W(E);
  } : typeof MessageChannel < "u" ? (T = new MessageChannel(), Y = T.port2, T.port1.onmessage = E, p = function() {
    Y.postMessage(null);
  }) : p = function() {
    z2(E, 0);
  };
  var T, Y;
  function M2(e2) {
    h2 = e2, w2 || (w2 = true, p());
  }
  function R(e2, n) {
    d = z2(function() {
      e2(r.unstable_now());
    }, n);
  }
  r.unstable_IdlePriority = 5;
  r.unstable_ImmediatePriority = 1;
  r.unstable_LowPriority = 4;
  r.unstable_NormalPriority = 3;
  r.unstable_Profiling = null;
  r.unstable_UserBlockingPriority = 2;
  r.unstable_cancelCallback = function(e2) {
    e2.callback = null;
  };
  r.unstable_continueExecution = function() {
    _ || P || (_ = true, M2(F2));
  };
  r.unstable_forceFrameRate = function(e2) {
    0 > e2 || 125 < e2 ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : G = 0 < e2 ? Math.floor(1e3 / e2) : 5;
  };
  r.unstable_getCurrentPriorityLevel = function() {
    return u;
  };
  r.unstable_getFirstCallbackNode = function() {
    return o(s);
  };
  r.unstable_next = function(e2) {
    switch (u) {
      case 1:
      case 2:
      case 3:
        var n = 3;
        break;
      default:
        n = u;
    }
    var t = u;
    u = n;
    try {
      return e2();
    } finally {
      u = t;
    }
  };
  r.unstable_pauseExecution = function() {
  };
  r.unstable_requestPaint = function() {
  };
  r.unstable_runWithPriority = function(e2, n) {
    switch (e2) {
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
        break;
      default:
        e2 = 3;
    }
    var t = u;
    u = e2;
    try {
      return n();
    } finally {
      u = t;
    }
  };
  r.unstable_scheduleCallback = function(e2, n, t) {
    var l = r.unstable_now();
    switch (typeof t == "object" && t !== null ? (t = t.delay, t = typeof t == "number" && 0 < t ? l + t : l) : t = l, e2) {
      case 1:
        var i = -1;
        break;
      case 2:
        i = 250;
        break;
      case 5:
        i = 1073741823;
        break;
      case 4:
        i = 1e4;
        break;
      default:
        i = 5e3;
    }
    return i = t + i, e2 = { id: te++, callback: n, priorityLevel: e2, startTime: t, expirationTime: i, sortIndex: -1 }, t > l ? (e2.sortIndex = t, L(c, e2), o(s) === null && e2 === o(c) && (v ? (A2(d), d = -1) : v = true, R(j, t - l))) : (e2.sortIndex = i, L(s, e2), _ || P || (_ = true, M2(F2))), e2;
  };
  r.unstable_shouldYield = J;
  r.unstable_wrapCallback = function(e2) {
    var n = u;
    return function() {
      var t = u;
      u = n;
      try {
        return e2.apply(this, arguments);
      } finally {
        u = t;
      }
    };
  };
});
var S = D((ie, Q) => {
  "use strict";
  Q.exports = K();
});
var x = ne(S());
var { unstable_now: ue, unstable_IdlePriority: ae2, unstable_ImmediatePriority: oe, unstable_LowPriority: se, unstable_NormalPriority: ce, unstable_Profiling: fe2, unstable_UserBlockingPriority: be2, unstable_cancelCallback: _e2, unstable_continueExecution: pe2, unstable_forceFrameRate: ve2, unstable_getCurrentPriorityLevel: de2, unstable_getFirstCallbackNode: ye2, unstable_next: me2, unstable_pauseExecution: ge2, unstable_requestPaint: he2, unstable_runWithPriority: ke2, unstable_scheduleCallback: Pe2, unstable_shouldYield: we2, unstable_wrapCallback: xe2 } = x;
var Ie2 = x.default ?? x;

// bigframes/display/react-dom.js
var require2 = (n) => {
  const e2 = (m) => typeof m.default < "u" ? m.default : m, c = (m) => Object.assign({ __esModule: true }, m);
  switch (n) {
    case "react":
      return e2(react_exports);
    case "scheduler":
      return e2(scheduler_exports);
    default:
      console.error('module "' + n + '" not found');
      return null;
  }
};
var ga = Object.create;
var lu = Object.defineProperty;
var wa = Object.getOwnPropertyDescriptor;
var Sa = Object.getOwnPropertyNames;
var ka = Object.getPrototypeOf;
var Ea = Object.prototype.hasOwnProperty;
var iu = ((e2) => typeof require2 < "u" ? require2 : typeof Proxy < "u" ? new Proxy(e2, { get: (n, t) => (typeof require2 < "u" ? require2 : n)[t] }) : e2)(function(e2) {
  if (typeof require2 < "u")
    return require2.apply(this, arguments);
  throw Error('Dynamic require of "' + e2 + '" is not supported');
});
var uu = (e2, n) => () => (n || e2((n = { exports: {} }).exports, n), n.exports);
var Ca = (e2, n, t, r) => {
  if (n && typeof n == "object" || typeof n == "function")
    for (let l of Sa(n))
      !Ea.call(e2, l) && l !== t && lu(e2, l, { get: () => n[l], enumerable: !(r = wa(n, l)) || r.enumerable });
  return e2;
};
var xa = (e2, n, t) => (t = e2 != null ? ga(ka(e2)) : {}, Ca(n || !e2 || !e2.__esModule ? lu(t, "default", { value: e2, enumerable: true }) : t, e2));
var pa = uu((fe3) => {
  "use strict";
  var mo = iu("react"), ae3 = iu("scheduler");
  function v(e2) {
    for (var n = "https://reactjs.org/docs/error-decoder.html?invariant=" + e2, t = 1; t < arguments.length; t++)
      n += "&args[]=" + encodeURIComponent(arguments[t]);
    return "Minified React error #" + e2 + "; visit " + n + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  var ho = new Set(), gt = {};
  function Sn(e2, n) {
    Hn(e2, n), Hn(e2 + "Capture", n);
  }
  function Hn(e2, n) {
    for (gt[e2] = n, e2 = 0; e2 < n.length; e2++)
      ho.add(n[e2]);
  }
  var Fe2 = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), El = Object.prototype.hasOwnProperty, Na = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, ou = {}, su = {};
  function _a(e2) {
    return El.call(su, e2) ? true : El.call(ou, e2) ? false : Na.test(e2) ? su[e2] = true : (ou[e2] = true, false);
  }
  function za(e2, n, t, r) {
    if (t !== null && t.type === 0)
      return false;
    switch (typeof n) {
      case "function":
      case "symbol":
        return true;
      case "boolean":
        return r ? false : t !== null ? !t.acceptsBooleans : (e2 = e2.toLowerCase().slice(0, 5), e2 !== "data-" && e2 !== "aria-");
      default:
        return false;
    }
  }
  function Pa(e2, n, t, r) {
    if (n === null || typeof n > "u" || za(e2, n, t, r))
      return true;
    if (r)
      return false;
    if (t !== null)
      switch (t.type) {
        case 3:
          return !n;
        case 4:
          return n === false;
        case 5:
          return isNaN(n);
        case 6:
          return isNaN(n) || 1 > n;
      }
    return false;
  }
  function ee2(e2, n, t, r, l, i, u) {
    this.acceptsBooleans = n === 2 || n === 3 || n === 4, this.attributeName = r, this.attributeNamespace = l, this.mustUseProperty = t, this.propertyName = e2, this.type = n, this.sanitizeURL = i, this.removeEmptyString = u;
  }
  var Y = {};
  "children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e2) {
    Y[e2] = new ee2(e2, 0, false, e2, null, false, false);
  });
  [["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e2) {
    var n = e2[0];
    Y[n] = new ee2(n, 1, false, e2[1], null, false, false);
  });
  ["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e2) {
    Y[e2] = new ee2(e2, 2, false, e2.toLowerCase(), null, false, false);
  });
  ["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e2) {
    Y[e2] = new ee2(e2, 2, false, e2, null, false, false);
  });
  "allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e2) {
    Y[e2] = new ee2(e2, 3, false, e2.toLowerCase(), null, false, false);
  });
  ["checked", "multiple", "muted", "selected"].forEach(function(e2) {
    Y[e2] = new ee2(e2, 3, true, e2, null, false, false);
  });
  ["capture", "download"].forEach(function(e2) {
    Y[e2] = new ee2(e2, 4, false, e2, null, false, false);
  });
  ["cols", "rows", "size", "span"].forEach(function(e2) {
    Y[e2] = new ee2(e2, 6, false, e2, null, false, false);
  });
  ["rowSpan", "start"].forEach(function(e2) {
    Y[e2] = new ee2(e2, 5, false, e2.toLowerCase(), null, false, false);
  });
  var mi = /[\-:]([a-z])/g;
  function hi(e2) {
    return e2[1].toUpperCase();
  }
  "accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e2) {
    var n = e2.replace(mi, hi);
    Y[n] = new ee2(n, 1, false, e2, null, false, false);
  });
  "xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e2) {
    var n = e2.replace(mi, hi);
    Y[n] = new ee2(n, 1, false, e2, "http://www.w3.org/1999/xlink", false, false);
  });
  ["xml:base", "xml:lang", "xml:space"].forEach(function(e2) {
    var n = e2.replace(mi, hi);
    Y[n] = new ee2(n, 1, false, e2, "http://www.w3.org/XML/1998/namespace", false, false);
  });
  ["tabIndex", "crossOrigin"].forEach(function(e2) {
    Y[e2] = new ee2(e2, 1, false, e2.toLowerCase(), null, false, false);
  });
  Y.xlinkHref = new ee2("xlinkHref", 1, false, "xlink:href", "http://www.w3.org/1999/xlink", true, false);
  ["src", "href", "action", "formAction"].forEach(function(e2) {
    Y[e2] = new ee2(e2, 1, false, e2.toLowerCase(), null, true, true);
  });
  function vi(e2, n, t, r) {
    var l = Y.hasOwnProperty(n) ? Y[n] : null;
    (l !== null ? l.type !== 0 : r || !(2 < n.length) || n[0] !== "o" && n[0] !== "O" || n[1] !== "n" && n[1] !== "N") && (Pa(n, t, l, r) && (t = null), r || l === null ? _a(n) && (t === null ? e2.removeAttribute(n) : e2.setAttribute(n, "" + t)) : l.mustUseProperty ? e2[l.propertyName] = t === null ? l.type === 3 ? false : "" : t : (n = l.attributeName, r = l.attributeNamespace, t === null ? e2.removeAttribute(n) : (l = l.type, t = l === 3 || l === 4 && t === true ? "" : "" + t, r ? e2.setAttributeNS(r, n, t) : e2.setAttribute(n, t))));
  }
  var Ve2 = mo.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, Vt = Symbol.for("react.element"), xn = Symbol.for("react.portal"), Nn = Symbol.for("react.fragment"), yi = Symbol.for("react.strict_mode"), Cl = Symbol.for("react.profiler"), vo = Symbol.for("react.provider"), yo = Symbol.for("react.context"), gi = Symbol.for("react.forward_ref"), xl = Symbol.for("react.suspense"), Nl = Symbol.for("react.suspense_list"), wi = Symbol.for("react.memo"), He = Symbol.for("react.lazy");
  Symbol.for("react.scope");
  Symbol.for("react.debug_trace_mode");
  var go = Symbol.for("react.offscreen");
  Symbol.for("react.legacy_hidden");
  Symbol.for("react.cache");
  Symbol.for("react.tracing_marker");
  var au = Symbol.iterator;
  function Jn(e2) {
    return e2 === null || typeof e2 != "object" ? null : (e2 = au && e2[au] || e2["@@iterator"], typeof e2 == "function" ? e2 : null);
  }
  var F2 = Object.assign, el;
  function it(e2) {
    if (el === void 0)
      try {
        throw Error();
      } catch (t) {
        var n = t.stack.trim().match(/\n( *(at )?)/);
        el = n && n[1] || "";
      }
    return `
` + el + e2;
  }
  var nl = false;
  function tl(e2, n) {
    if (!e2 || nl)
      return "";
    nl = true;
    var t = Error.prepareStackTrace;
    Error.prepareStackTrace = void 0;
    try {
      if (n)
        if (n = function() {
          throw Error();
        }, Object.defineProperty(n.prototype, "props", { set: function() {
          throw Error();
        } }), typeof Reflect == "object" && Reflect.construct) {
          try {
            Reflect.construct(n, []);
          } catch (d) {
            var r = d;
          }
          Reflect.construct(e2, [], n);
        } else {
          try {
            n.call();
          } catch (d) {
            r = d;
          }
          e2.call(n.prototype);
        }
      else {
        try {
          throw Error();
        } catch (d) {
          r = d;
        }
        e2();
      }
    } catch (d) {
      if (d && r && typeof d.stack == "string") {
        for (var l = d.stack.split(`
`), i = r.stack.split(`
`), u = l.length - 1, o = i.length - 1; 1 <= u && 0 <= o && l[u] !== i[o]; )
          o--;
        for (; 1 <= u && 0 <= o; u--, o--)
          if (l[u] !== i[o]) {
            if (u !== 1 || o !== 1)
              do
                if (u--, o--, 0 > o || l[u] !== i[o]) {
                  var s = `
` + l[u].replace(" at new ", " at ");
                  return e2.displayName && s.includes("<anonymous>") && (s = s.replace("<anonymous>", e2.displayName)), s;
                }
              while (1 <= u && 0 <= o);
            break;
          }
      }
    } finally {
      nl = false, Error.prepareStackTrace = t;
    }
    return (e2 = e2 ? e2.displayName || e2.name : "") ? it(e2) : "";
  }
  function La(e2) {
    switch (e2.tag) {
      case 5:
        return it(e2.type);
      case 16:
        return it("Lazy");
      case 13:
        return it("Suspense");
      case 19:
        return it("SuspenseList");
      case 0:
      case 2:
      case 15:
        return e2 = tl(e2.type, false), e2;
      case 11:
        return e2 = tl(e2.type.render, false), e2;
      case 1:
        return e2 = tl(e2.type, true), e2;
      default:
        return "";
    }
  }
  function _l(e2) {
    if (e2 == null)
      return null;
    if (typeof e2 == "function")
      return e2.displayName || e2.name || null;
    if (typeof e2 == "string")
      return e2;
    switch (e2) {
      case Nn:
        return "Fragment";
      case xn:
        return "Portal";
      case Cl:
        return "Profiler";
      case yi:
        return "StrictMode";
      case xl:
        return "Suspense";
      case Nl:
        return "SuspenseList";
    }
    if (typeof e2 == "object")
      switch (e2.$$typeof) {
        case yo:
          return (e2.displayName || "Context") + ".Consumer";
        case vo:
          return (e2._context.displayName || "Context") + ".Provider";
        case gi:
          var n = e2.render;
          return e2 = e2.displayName, e2 || (e2 = n.displayName || n.name || "", e2 = e2 !== "" ? "ForwardRef(" + e2 + ")" : "ForwardRef"), e2;
        case wi:
          return n = e2.displayName || null, n !== null ? n : _l(e2.type) || "Memo";
        case He:
          n = e2._payload, e2 = e2._init;
          try {
            return _l(e2(n));
          } catch {
          }
      }
    return null;
  }
  function Ta(e2) {
    var n = e2.type;
    switch (e2.tag) {
      case 24:
        return "Cache";
      case 9:
        return (n.displayName || "Context") + ".Consumer";
      case 10:
        return (n._context.displayName || "Context") + ".Provider";
      case 18:
        return "DehydratedFragment";
      case 11:
        return e2 = n.render, e2 = e2.displayName || e2.name || "", n.displayName || (e2 !== "" ? "ForwardRef(" + e2 + ")" : "ForwardRef");
      case 7:
        return "Fragment";
      case 5:
        return n;
      case 4:
        return "Portal";
      case 3:
        return "Root";
      case 6:
        return "Text";
      case 16:
        return _l(n);
      case 8:
        return n === yi ? "StrictMode" : "Mode";
      case 22:
        return "Offscreen";
      case 12:
        return "Profiler";
      case 21:
        return "Scope";
      case 13:
        return "Suspense";
      case 19:
        return "SuspenseList";
      case 25:
        return "TracingMarker";
      case 1:
      case 0:
      case 17:
      case 2:
      case 14:
      case 15:
        if (typeof n == "function")
          return n.displayName || n.name || null;
        if (typeof n == "string")
          return n;
    }
    return null;
  }
  function tn(e2) {
    switch (typeof e2) {
      case "boolean":
      case "number":
      case "string":
      case "undefined":
        return e2;
      case "object":
        return e2;
      default:
        return "";
    }
  }
  function wo(e2) {
    var n = e2.type;
    return (e2 = e2.nodeName) && e2.toLowerCase() === "input" && (n === "checkbox" || n === "radio");
  }
  function Ma(e2) {
    var n = wo(e2) ? "checked" : "value", t = Object.getOwnPropertyDescriptor(e2.constructor.prototype, n), r = "" + e2[n];
    if (!e2.hasOwnProperty(n) && typeof t < "u" && typeof t.get == "function" && typeof t.set == "function") {
      var l = t.get, i = t.set;
      return Object.defineProperty(e2, n, { configurable: true, get: function() {
        return l.call(this);
      }, set: function(u) {
        r = "" + u, i.call(this, u);
      } }), Object.defineProperty(e2, n, { enumerable: t.enumerable }), { getValue: function() {
        return r;
      }, setValue: function(u) {
        r = "" + u;
      }, stopTracking: function() {
        e2._valueTracker = null, delete e2[n];
      } };
    }
  }
  function At(e2) {
    e2._valueTracker || (e2._valueTracker = Ma(e2));
  }
  function So(e2) {
    if (!e2)
      return false;
    var n = e2._valueTracker;
    if (!n)
      return true;
    var t = n.getValue(), r = "";
    return e2 && (r = wo(e2) ? e2.checked ? "true" : "false" : e2.value), e2 = r, e2 !== t ? (n.setValue(e2), true) : false;
  }
  function mr(e2) {
    if (e2 = e2 || (typeof document < "u" ? document : void 0), typeof e2 > "u")
      return null;
    try {
      return e2.activeElement || e2.body;
    } catch {
      return e2.body;
    }
  }
  function zl(e2, n) {
    var t = n.checked;
    return F2({}, n, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: t ?? e2._wrapperState.initialChecked });
  }
  function cu(e2, n) {
    var t = n.defaultValue == null ? "" : n.defaultValue, r = n.checked != null ? n.checked : n.defaultChecked;
    t = tn(n.value != null ? n.value : t), e2._wrapperState = { initialChecked: r, initialValue: t, controlled: n.type === "checkbox" || n.type === "radio" ? n.checked != null : n.value != null };
  }
  function ko(e2, n) {
    n = n.checked, n != null && vi(e2, "checked", n, false);
  }
  function Pl(e2, n) {
    ko(e2, n);
    var t = tn(n.value), r = n.type;
    if (t != null)
      r === "number" ? (t === 0 && e2.value === "" || e2.value != t) && (e2.value = "" + t) : e2.value !== "" + t && (e2.value = "" + t);
    else if (r === "submit" || r === "reset") {
      e2.removeAttribute("value");
      return;
    }
    n.hasOwnProperty("value") ? Ll(e2, n.type, t) : n.hasOwnProperty("defaultValue") && Ll(e2, n.type, tn(n.defaultValue)), n.checked == null && n.defaultChecked != null && (e2.defaultChecked = !!n.defaultChecked);
  }
  function fu(e2, n, t) {
    if (n.hasOwnProperty("value") || n.hasOwnProperty("defaultValue")) {
      var r = n.type;
      if (!(r !== "submit" && r !== "reset" || n.value !== void 0 && n.value !== null))
        return;
      n = "" + e2._wrapperState.initialValue, t || n === e2.value || (e2.value = n), e2.defaultValue = n;
    }
    t = e2.name, t !== "" && (e2.name = ""), e2.defaultChecked = !!e2._wrapperState.initialChecked, t !== "" && (e2.name = t);
  }
  function Ll(e2, n, t) {
    (n !== "number" || mr(e2.ownerDocument) !== e2) && (t == null ? e2.defaultValue = "" + e2._wrapperState.initialValue : e2.defaultValue !== "" + t && (e2.defaultValue = "" + t));
  }
  var ut = Array.isArray;
  function In(e2, n, t, r) {
    if (e2 = e2.options, n) {
      n = {};
      for (var l = 0; l < t.length; l++)
        n["$" + t[l]] = true;
      for (t = 0; t < e2.length; t++)
        l = n.hasOwnProperty("$" + e2[t].value), e2[t].selected !== l && (e2[t].selected = l), l && r && (e2[t].defaultSelected = true);
    } else {
      for (t = "" + tn(t), n = null, l = 0; l < e2.length; l++) {
        if (e2[l].value === t) {
          e2[l].selected = true, r && (e2[l].defaultSelected = true);
          return;
        }
        n !== null || e2[l].disabled || (n = e2[l]);
      }
      n !== null && (n.selected = true);
    }
  }
  function Tl(e2, n) {
    if (n.dangerouslySetInnerHTML != null)
      throw Error(v(91));
    return F2({}, n, { value: void 0, defaultValue: void 0, children: "" + e2._wrapperState.initialValue });
  }
  function du(e2, n) {
    var t = n.value;
    if (t == null) {
      if (t = n.children, n = n.defaultValue, t != null) {
        if (n != null)
          throw Error(v(92));
        if (ut(t)) {
          if (1 < t.length)
            throw Error(v(93));
          t = t[0];
        }
        n = t;
      }
      n == null && (n = ""), t = n;
    }
    e2._wrapperState = { initialValue: tn(t) };
  }
  function Eo(e2, n) {
    var t = tn(n.value), r = tn(n.defaultValue);
    t != null && (t = "" + t, t !== e2.value && (e2.value = t), n.defaultValue == null && e2.defaultValue !== t && (e2.defaultValue = t)), r != null && (e2.defaultValue = "" + r);
  }
  function pu(e2) {
    var n = e2.textContent;
    n === e2._wrapperState.initialValue && n !== "" && n !== null && (e2.value = n);
  }
  function Co(e2) {
    switch (e2) {
      case "svg":
        return "http://www.w3.org/2000/svg";
      case "math":
        return "http://www.w3.org/1998/Math/MathML";
      default:
        return "http://www.w3.org/1999/xhtml";
    }
  }
  function Ml(e2, n) {
    return e2 == null || e2 === "http://www.w3.org/1999/xhtml" ? Co(n) : e2 === "http://www.w3.org/2000/svg" && n === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e2;
  }
  var Bt, xo = function(e2) {
    return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(n, t, r, l) {
      MSApp.execUnsafeLocalFunction(function() {
        return e2(n, t, r, l);
      });
    } : e2;
  }(function(e2, n) {
    if (e2.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in e2)
      e2.innerHTML = n;
    else {
      for (Bt = Bt || document.createElement("div"), Bt.innerHTML = "<svg>" + n.valueOf().toString() + "</svg>", n = Bt.firstChild; e2.firstChild; )
        e2.removeChild(e2.firstChild);
      for (; n.firstChild; )
        e2.appendChild(n.firstChild);
    }
  });
  function wt(e2, n) {
    if (n) {
      var t = e2.firstChild;
      if (t && t === e2.lastChild && t.nodeType === 3) {
        t.nodeValue = n;
        return;
      }
    }
    e2.textContent = n;
  }
  var at = { animationIterationCount: true, aspectRatio: true, borderImageOutset: true, borderImageSlice: true, borderImageWidth: true, boxFlex: true, boxFlexGroup: true, boxOrdinalGroup: true, columnCount: true, columns: true, flex: true, flexGrow: true, flexPositive: true, flexShrink: true, flexNegative: true, flexOrder: true, gridArea: true, gridRow: true, gridRowEnd: true, gridRowSpan: true, gridRowStart: true, gridColumn: true, gridColumnEnd: true, gridColumnSpan: true, gridColumnStart: true, fontWeight: true, lineClamp: true, lineHeight: true, opacity: true, order: true, orphans: true, tabSize: true, widows: true, zIndex: true, zoom: true, fillOpacity: true, floodOpacity: true, stopOpacity: true, strokeDasharray: true, strokeDashoffset: true, strokeMiterlimit: true, strokeOpacity: true, strokeWidth: true }, Da = ["Webkit", "ms", "Moz", "O"];
  Object.keys(at).forEach(function(e2) {
    Da.forEach(function(n) {
      n = n + e2.charAt(0).toUpperCase() + e2.substring(1), at[n] = at[e2];
    });
  });
  function No(e2, n, t) {
    return n == null || typeof n == "boolean" || n === "" ? "" : t || typeof n != "number" || n === 0 || at.hasOwnProperty(e2) && at[e2] ? ("" + n).trim() : n + "px";
  }
  function _o(e2, n) {
    e2 = e2.style;
    for (var t in n)
      if (n.hasOwnProperty(t)) {
        var r = t.indexOf("--") === 0, l = No(t, n[t], r);
        t === "float" && (t = "cssFloat"), r ? e2.setProperty(t, l) : e2[t] = l;
      }
  }
  var Oa = F2({ menuitem: true }, { area: true, base: true, br: true, col: true, embed: true, hr: true, img: true, input: true, keygen: true, link: true, meta: true, param: true, source: true, track: true, wbr: true });
  function Dl(e2, n) {
    if (n) {
      if (Oa[e2] && (n.children != null || n.dangerouslySetInnerHTML != null))
        throw Error(v(137, e2));
      if (n.dangerouslySetInnerHTML != null) {
        if (n.children != null)
          throw Error(v(60));
        if (typeof n.dangerouslySetInnerHTML != "object" || !("__html" in n.dangerouslySetInnerHTML))
          throw Error(v(61));
      }
      if (n.style != null && typeof n.style != "object")
        throw Error(v(62));
    }
  }
  function Ol(e2, n) {
    if (e2.indexOf("-") === -1)
      return typeof n.is == "string";
    switch (e2) {
      case "annotation-xml":
      case "color-profile":
      case "font-face":
      case "font-face-src":
      case "font-face-uri":
      case "font-face-format":
      case "font-face-name":
      case "missing-glyph":
        return false;
      default:
        return true;
    }
  }
  var Rl = null;
  function Si(e2) {
    return e2 = e2.target || e2.srcElement || window, e2.correspondingUseElement && (e2 = e2.correspondingUseElement), e2.nodeType === 3 ? e2.parentNode : e2;
  }
  var Fl = null, jn = null, Un = null;
  function mu(e2) {
    if (e2 = jt(e2)) {
      if (typeof Fl != "function")
        throw Error(v(280));
      var n = e2.stateNode;
      n && (n = Hr(n), Fl(e2.stateNode, e2.type, n));
    }
  }
  function zo(e2) {
    jn ? Un ? Un.push(e2) : Un = [e2] : jn = e2;
  }
  function Po() {
    if (jn) {
      var e2 = jn, n = Un;
      if (Un = jn = null, mu(e2), n)
        for (e2 = 0; e2 < n.length; e2++)
          mu(n[e2]);
    }
  }
  function Lo(e2, n) {
    return e2(n);
  }
  function To() {
  }
  var rl = false;
  function Mo(e2, n, t) {
    if (rl)
      return e2(n, t);
    rl = true;
    try {
      return Lo(e2, n, t);
    } finally {
      rl = false, (jn !== null || Un !== null) && (To(), Po());
    }
  }
  function St(e2, n) {
    var t = e2.stateNode;
    if (t === null)
      return null;
    var r = Hr(t);
    if (r === null)
      return null;
    t = r[n];
    e:
      switch (n) {
        case "onClick":
        case "onClickCapture":
        case "onDoubleClick":
        case "onDoubleClickCapture":
        case "onMouseDown":
        case "onMouseDownCapture":
        case "onMouseMove":
        case "onMouseMoveCapture":
        case "onMouseUp":
        case "onMouseUpCapture":
        case "onMouseEnter":
          (r = !r.disabled) || (e2 = e2.type, r = !(e2 === "button" || e2 === "input" || e2 === "select" || e2 === "textarea")), e2 = !r;
          break e;
        default:
          e2 = false;
      }
    if (e2)
      return null;
    if (t && typeof t != "function")
      throw Error(v(231, n, typeof t));
    return t;
  }
  var Il = false;
  if (Fe2)
    try {
      En = {}, Object.defineProperty(En, "passive", { get: function() {
        Il = true;
      } }), window.addEventListener("test", En, En), window.removeEventListener("test", En, En);
    } catch {
      Il = false;
    }
  var En;
  function Ra(e2, n, t, r, l, i, u, o, s) {
    var d = Array.prototype.slice.call(arguments, 3);
    try {
      n.apply(t, d);
    } catch (m) {
      this.onError(m);
    }
  }
  var ct = false, hr = null, vr = false, jl = null, Fa = { onError: function(e2) {
    ct = true, hr = e2;
  } };
  function Ia(e2, n, t, r, l, i, u, o, s) {
    ct = false, hr = null, Ra.apply(Fa, arguments);
  }
  function ja(e2, n, t, r, l, i, u, o, s) {
    if (Ia.apply(this, arguments), ct) {
      if (ct) {
        var d = hr;
        ct = false, hr = null;
      } else
        throw Error(v(198));
      vr || (vr = true, jl = d);
    }
  }
  function kn(e2) {
    var n = e2, t = e2;
    if (e2.alternate)
      for (; n.return; )
        n = n.return;
    else {
      e2 = n;
      do
        n = e2, (n.flags & 4098) !== 0 && (t = n.return), e2 = n.return;
      while (e2);
    }
    return n.tag === 3 ? t : null;
  }
  function Do(e2) {
    if (e2.tag === 13) {
      var n = e2.memoizedState;
      if (n === null && (e2 = e2.alternate, e2 !== null && (n = e2.memoizedState)), n !== null)
        return n.dehydrated;
    }
    return null;
  }
  function hu(e2) {
    if (kn(e2) !== e2)
      throw Error(v(188));
  }
  function Ua(e2) {
    var n = e2.alternate;
    if (!n) {
      if (n = kn(e2), n === null)
        throw Error(v(188));
      return n !== e2 ? null : e2;
    }
    for (var t = e2, r = n; ; ) {
      var l = t.return;
      if (l === null)
        break;
      var i = l.alternate;
      if (i === null) {
        if (r = l.return, r !== null) {
          t = r;
          continue;
        }
        break;
      }
      if (l.child === i.child) {
        for (i = l.child; i; ) {
          if (i === t)
            return hu(l), e2;
          if (i === r)
            return hu(l), n;
          i = i.sibling;
        }
        throw Error(v(188));
      }
      if (t.return !== r.return)
        t = l, r = i;
      else {
        for (var u = false, o = l.child; o; ) {
          if (o === t) {
            u = true, t = l, r = i;
            break;
          }
          if (o === r) {
            u = true, r = l, t = i;
            break;
          }
          o = o.sibling;
        }
        if (!u) {
          for (o = i.child; o; ) {
            if (o === t) {
              u = true, t = i, r = l;
              break;
            }
            if (o === r) {
              u = true, r = i, t = l;
              break;
            }
            o = o.sibling;
          }
          if (!u)
            throw Error(v(189));
        }
      }
      if (t.alternate !== r)
        throw Error(v(190));
    }
    if (t.tag !== 3)
      throw Error(v(188));
    return t.stateNode.current === t ? e2 : n;
  }
  function Oo(e2) {
    return e2 = Ua(e2), e2 !== null ? Ro(e2) : null;
  }
  function Ro(e2) {
    if (e2.tag === 5 || e2.tag === 6)
      return e2;
    for (e2 = e2.child; e2 !== null; ) {
      var n = Ro(e2);
      if (n !== null)
        return n;
      e2 = e2.sibling;
    }
    return null;
  }
  var Fo = ae3.unstable_scheduleCallback, vu = ae3.unstable_cancelCallback, Va = ae3.unstable_shouldYield, Aa = ae3.unstable_requestPaint, U3 = ae3.unstable_now, Ba = ae3.unstable_getCurrentPriorityLevel, ki = ae3.unstable_ImmediatePriority, Io = ae3.unstable_UserBlockingPriority, yr = ae3.unstable_NormalPriority, Ha = ae3.unstable_LowPriority, jo = ae3.unstable_IdlePriority, Ur = null, Pe3 = null;
  function Wa(e2) {
    if (Pe3 && typeof Pe3.onCommitFiberRoot == "function")
      try {
        Pe3.onCommitFiberRoot(Ur, e2, void 0, (e2.current.flags & 128) === 128);
      } catch {
      }
  }
  var Ee2 = Math.clz32 ? Math.clz32 : Ka, Qa = Math.log, $a = Math.LN2;
  function Ka(e2) {
    return e2 >>>= 0, e2 === 0 ? 32 : 31 - (Qa(e2) / $a | 0) | 0;
  }
  var Ht = 64, Wt = 4194304;
  function ot(e2) {
    switch (e2 & -e2) {
      case 1:
        return 1;
      case 2:
        return 2;
      case 4:
        return 4;
      case 8:
        return 8;
      case 16:
        return 16;
      case 32:
        return 32;
      case 64:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return e2 & 4194240;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return e2 & 130023424;
      case 134217728:
        return 134217728;
      case 268435456:
        return 268435456;
      case 536870912:
        return 536870912;
      case 1073741824:
        return 1073741824;
      default:
        return e2;
    }
  }
  function gr(e2, n) {
    var t = e2.pendingLanes;
    if (t === 0)
      return 0;
    var r = 0, l = e2.suspendedLanes, i = e2.pingedLanes, u = t & 268435455;
    if (u !== 0) {
      var o = u & ~l;
      o !== 0 ? r = ot(o) : (i &= u, i !== 0 && (r = ot(i)));
    } else
      u = t & ~l, u !== 0 ? r = ot(u) : i !== 0 && (r = ot(i));
    if (r === 0)
      return 0;
    if (n !== 0 && n !== r && (n & l) === 0 && (l = r & -r, i = n & -n, l >= i || l === 16 && (i & 4194240) !== 0))
      return n;
    if ((r & 4) !== 0 && (r |= t & 16), n = e2.entangledLanes, n !== 0)
      for (e2 = e2.entanglements, n &= r; 0 < n; )
        t = 31 - Ee2(n), l = 1 << t, r |= e2[t], n &= ~l;
    return r;
  }
  function Ya(e2, n) {
    switch (e2) {
      case 1:
      case 2:
      case 4:
        return n + 250;
      case 8:
      case 16:
      case 32:
      case 64:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return n + 5e3;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return -1;
      case 134217728:
      case 268435456:
      case 536870912:
      case 1073741824:
        return -1;
      default:
        return -1;
    }
  }
  function Xa(e2, n) {
    for (var t = e2.suspendedLanes, r = e2.pingedLanes, l = e2.expirationTimes, i = e2.pendingLanes; 0 < i; ) {
      var u = 31 - Ee2(i), o = 1 << u, s = l[u];
      s === -1 ? ((o & t) === 0 || (o & r) !== 0) && (l[u] = Ya(o, n)) : s <= n && (e2.expiredLanes |= o), i &= ~o;
    }
  }
  function Ul(e2) {
    return e2 = e2.pendingLanes & -1073741825, e2 !== 0 ? e2 : e2 & 1073741824 ? 1073741824 : 0;
  }
  function Uo() {
    var e2 = Ht;
    return Ht <<= 1, (Ht & 4194240) === 0 && (Ht = 64), e2;
  }
  function ll(e2) {
    for (var n = [], t = 0; 31 > t; t++)
      n.push(e2);
    return n;
  }
  function Ft(e2, n, t) {
    e2.pendingLanes |= n, n !== 536870912 && (e2.suspendedLanes = 0, e2.pingedLanes = 0), e2 = e2.eventTimes, n = 31 - Ee2(n), e2[n] = t;
  }
  function Ga(e2, n) {
    var t = e2.pendingLanes & ~n;
    e2.pendingLanes = n, e2.suspendedLanes = 0, e2.pingedLanes = 0, e2.expiredLanes &= n, e2.mutableReadLanes &= n, e2.entangledLanes &= n, n = e2.entanglements;
    var r = e2.eventTimes;
    for (e2 = e2.expirationTimes; 0 < t; ) {
      var l = 31 - Ee2(t), i = 1 << l;
      n[l] = 0, r[l] = -1, e2[l] = -1, t &= ~i;
    }
  }
  function Ei(e2, n) {
    var t = e2.entangledLanes |= n;
    for (e2 = e2.entanglements; t; ) {
      var r = 31 - Ee2(t), l = 1 << r;
      l & n | e2[r] & n && (e2[r] |= n), t &= ~l;
    }
  }
  var P = 0;
  function Vo(e2) {
    return e2 &= -e2, 1 < e2 ? 4 < e2 ? (e2 & 268435455) !== 0 ? 16 : 536870912 : 4 : 1;
  }
  var Ao, Ci, Bo, Ho, Wo, Vl = false, Qt = [], Xe = null, Ge = null, Ze = null, kt = new Map(), Et = new Map(), Qe = [], Za = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
  function yu(e2, n) {
    switch (e2) {
      case "focusin":
      case "focusout":
        Xe = null;
        break;
      case "dragenter":
      case "dragleave":
        Ge = null;
        break;
      case "mouseover":
      case "mouseout":
        Ze = null;
        break;
      case "pointerover":
      case "pointerout":
        kt.delete(n.pointerId);
        break;
      case "gotpointercapture":
      case "lostpointercapture":
        Et.delete(n.pointerId);
    }
  }
  function qn(e2, n, t, r, l, i) {
    return e2 === null || e2.nativeEvent !== i ? (e2 = { blockedOn: n, domEventName: t, eventSystemFlags: r, nativeEvent: i, targetContainers: [l] }, n !== null && (n = jt(n), n !== null && Ci(n)), e2) : (e2.eventSystemFlags |= r, n = e2.targetContainers, l !== null && n.indexOf(l) === -1 && n.push(l), e2);
  }
  function Ja(e2, n, t, r, l) {
    switch (n) {
      case "focusin":
        return Xe = qn(Xe, e2, n, t, r, l), true;
      case "dragenter":
        return Ge = qn(Ge, e2, n, t, r, l), true;
      case "mouseover":
        return Ze = qn(Ze, e2, n, t, r, l), true;
      case "pointerover":
        var i = l.pointerId;
        return kt.set(i, qn(kt.get(i) || null, e2, n, t, r, l)), true;
      case "gotpointercapture":
        return i = l.pointerId, Et.set(i, qn(Et.get(i) || null, e2, n, t, r, l)), true;
    }
    return false;
  }
  function Qo(e2) {
    var n = cn(e2.target);
    if (n !== null) {
      var t = kn(n);
      if (t !== null) {
        if (n = t.tag, n === 13) {
          if (n = Do(t), n !== null) {
            e2.blockedOn = n, Wo(e2.priority, function() {
              Bo(t);
            });
            return;
          }
        } else if (n === 3 && t.stateNode.current.memoizedState.isDehydrated) {
          e2.blockedOn = t.tag === 3 ? t.stateNode.containerInfo : null;
          return;
        }
      }
    }
    e2.blockedOn = null;
  }
  function lr(e2) {
    if (e2.blockedOn !== null)
      return false;
    for (var n = e2.targetContainers; 0 < n.length; ) {
      var t = Al(e2.domEventName, e2.eventSystemFlags, n[0], e2.nativeEvent);
      if (t === null) {
        t = e2.nativeEvent;
        var r = new t.constructor(t.type, t);
        Rl = r, t.target.dispatchEvent(r), Rl = null;
      } else
        return n = jt(t), n !== null && Ci(n), e2.blockedOn = t, false;
      n.shift();
    }
    return true;
  }
  function gu(e2, n, t) {
    lr(e2) && t.delete(n);
  }
  function qa() {
    Vl = false, Xe !== null && lr(Xe) && (Xe = null), Ge !== null && lr(Ge) && (Ge = null), Ze !== null && lr(Ze) && (Ze = null), kt.forEach(gu), Et.forEach(gu);
  }
  function bn(e2, n) {
    e2.blockedOn === n && (e2.blockedOn = null, Vl || (Vl = true, ae3.unstable_scheduleCallback(ae3.unstable_NormalPriority, qa)));
  }
  function Ct(e2) {
    function n(l) {
      return bn(l, e2);
    }
    if (0 < Qt.length) {
      bn(Qt[0], e2);
      for (var t = 1; t < Qt.length; t++) {
        var r = Qt[t];
        r.blockedOn === e2 && (r.blockedOn = null);
      }
    }
    for (Xe !== null && bn(Xe, e2), Ge !== null && bn(Ge, e2), Ze !== null && bn(Ze, e2), kt.forEach(n), Et.forEach(n), t = 0; t < Qe.length; t++)
      r = Qe[t], r.blockedOn === e2 && (r.blockedOn = null);
    for (; 0 < Qe.length && (t = Qe[0], t.blockedOn === null); )
      Qo(t), t.blockedOn === null && Qe.shift();
  }
  var Vn = Ve2.ReactCurrentBatchConfig, wr = true;
  function ba(e2, n, t, r) {
    var l = P, i = Vn.transition;
    Vn.transition = null;
    try {
      P = 1, xi(e2, n, t, r);
    } finally {
      P = l, Vn.transition = i;
    }
  }
  function ec(e2, n, t, r) {
    var l = P, i = Vn.transition;
    Vn.transition = null;
    try {
      P = 4, xi(e2, n, t, r);
    } finally {
      P = l, Vn.transition = i;
    }
  }
  function xi(e2, n, t, r) {
    if (wr) {
      var l = Al(e2, n, t, r);
      if (l === null)
        fl(e2, n, r, Sr, t), yu(e2, r);
      else if (Ja(l, e2, n, t, r))
        r.stopPropagation();
      else if (yu(e2, r), n & 4 && -1 < Za.indexOf(e2)) {
        for (; l !== null; ) {
          var i = jt(l);
          if (i !== null && Ao(i), i = Al(e2, n, t, r), i === null && fl(e2, n, r, Sr, t), i === l)
            break;
          l = i;
        }
        l !== null && r.stopPropagation();
      } else
        fl(e2, n, r, null, t);
    }
  }
  var Sr = null;
  function Al(e2, n, t, r) {
    if (Sr = null, e2 = Si(r), e2 = cn(e2), e2 !== null)
      if (n = kn(e2), n === null)
        e2 = null;
      else if (t = n.tag, t === 13) {
        if (e2 = Do(n), e2 !== null)
          return e2;
        e2 = null;
      } else if (t === 3) {
        if (n.stateNode.current.memoizedState.isDehydrated)
          return n.tag === 3 ? n.stateNode.containerInfo : null;
        e2 = null;
      } else
        n !== e2 && (e2 = null);
    return Sr = e2, null;
  }
  function $o(e2) {
    switch (e2) {
      case "cancel":
      case "click":
      case "close":
      case "contextmenu":
      case "copy":
      case "cut":
      case "auxclick":
      case "dblclick":
      case "dragend":
      case "dragstart":
      case "drop":
      case "focusin":
      case "focusout":
      case "input":
      case "invalid":
      case "keydown":
      case "keypress":
      case "keyup":
      case "mousedown":
      case "mouseup":
      case "paste":
      case "pause":
      case "play":
      case "pointercancel":
      case "pointerdown":
      case "pointerup":
      case "ratechange":
      case "reset":
      case "resize":
      case "seeked":
      case "submit":
      case "touchcancel":
      case "touchend":
      case "touchstart":
      case "volumechange":
      case "change":
      case "selectionchange":
      case "textInput":
      case "compositionstart":
      case "compositionend":
      case "compositionupdate":
      case "beforeblur":
      case "afterblur":
      case "beforeinput":
      case "blur":
      case "fullscreenchange":
      case "focus":
      case "hashchange":
      case "popstate":
      case "select":
      case "selectstart":
        return 1;
      case "drag":
      case "dragenter":
      case "dragexit":
      case "dragleave":
      case "dragover":
      case "mousemove":
      case "mouseout":
      case "mouseover":
      case "pointermove":
      case "pointerout":
      case "pointerover":
      case "scroll":
      case "toggle":
      case "touchmove":
      case "wheel":
      case "mouseenter":
      case "mouseleave":
      case "pointerenter":
      case "pointerleave":
        return 4;
      case "message":
        switch (Ba()) {
          case ki:
            return 1;
          case Io:
            return 4;
          case yr:
          case Ha:
            return 16;
          case jo:
            return 536870912;
          default:
            return 16;
        }
      default:
        return 16;
    }
  }
  var Ke = null, Ni = null, ir = null;
  function Ko() {
    if (ir)
      return ir;
    var e2, n = Ni, t = n.length, r, l = "value" in Ke ? Ke.value : Ke.textContent, i = l.length;
    for (e2 = 0; e2 < t && n[e2] === l[e2]; e2++)
      ;
    var u = t - e2;
    for (r = 1; r <= u && n[t - r] === l[i - r]; r++)
      ;
    return ir = l.slice(e2, 1 < r ? 1 - r : void 0);
  }
  function ur(e2) {
    var n = e2.keyCode;
    return "charCode" in e2 ? (e2 = e2.charCode, e2 === 0 && n === 13 && (e2 = 13)) : e2 = n, e2 === 10 && (e2 = 13), 32 <= e2 || e2 === 13 ? e2 : 0;
  }
  function $t() {
    return true;
  }
  function wu() {
    return false;
  }
  function ce2(e2) {
    function n(t, r, l, i, u) {
      this._reactName = t, this._targetInst = l, this.type = r, this.nativeEvent = i, this.target = u, this.currentTarget = null;
      for (var o in e2)
        e2.hasOwnProperty(o) && (t = e2[o], this[o] = t ? t(i) : i[o]);
      return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === false) ? $t : wu, this.isPropagationStopped = wu, this;
    }
    return F2(n.prototype, { preventDefault: function() {
      this.defaultPrevented = true;
      var t = this.nativeEvent;
      t && (t.preventDefault ? t.preventDefault() : typeof t.returnValue != "unknown" && (t.returnValue = false), this.isDefaultPrevented = $t);
    }, stopPropagation: function() {
      var t = this.nativeEvent;
      t && (t.stopPropagation ? t.stopPropagation() : typeof t.cancelBubble != "unknown" && (t.cancelBubble = true), this.isPropagationStopped = $t);
    }, persist: function() {
    }, isPersistent: $t }), n;
  }
  var Gn = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e2) {
    return e2.timeStamp || Date.now();
  }, defaultPrevented: 0, isTrusted: 0 }, _i = ce2(Gn), It = F2({}, Gn, { view: 0, detail: 0 }), nc = ce2(It), il, ul, et, Vr = F2({}, It, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: zi, button: 0, buttons: 0, relatedTarget: function(e2) {
    return e2.relatedTarget === void 0 ? e2.fromElement === e2.srcElement ? e2.toElement : e2.fromElement : e2.relatedTarget;
  }, movementX: function(e2) {
    return "movementX" in e2 ? e2.movementX : (e2 !== et && (et && e2.type === "mousemove" ? (il = e2.screenX - et.screenX, ul = e2.screenY - et.screenY) : ul = il = 0, et = e2), il);
  }, movementY: function(e2) {
    return "movementY" in e2 ? e2.movementY : ul;
  } }), Su = ce2(Vr), tc = F2({}, Vr, { dataTransfer: 0 }), rc = ce2(tc), lc = F2({}, It, { relatedTarget: 0 }), ol = ce2(lc), ic = F2({}, Gn, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), uc = ce2(ic), oc = F2({}, Gn, { clipboardData: function(e2) {
    return "clipboardData" in e2 ? e2.clipboardData : window.clipboardData;
  } }), sc = ce2(oc), ac = F2({}, Gn, { data: 0 }), ku = ce2(ac), cc = { Esc: "Escape", Spacebar: " ", Left: "ArrowLeft", Up: "ArrowUp", Right: "ArrowRight", Down: "ArrowDown", Del: "Delete", Win: "OS", Menu: "ContextMenu", Apps: "ContextMenu", Scroll: "ScrollLock", MozPrintableKey: "Unidentified" }, fc = { 8: "Backspace", 9: "Tab", 12: "Clear", 13: "Enter", 16: "Shift", 17: "Control", 18: "Alt", 19: "Pause", 20: "CapsLock", 27: "Escape", 32: " ", 33: "PageUp", 34: "PageDown", 35: "End", 36: "Home", 37: "ArrowLeft", 38: "ArrowUp", 39: "ArrowRight", 40: "ArrowDown", 45: "Insert", 46: "Delete", 112: "F1", 113: "F2", 114: "F3", 115: "F4", 116: "F5", 117: "F6", 118: "F7", 119: "F8", 120: "F9", 121: "F10", 122: "F11", 123: "F12", 144: "NumLock", 145: "ScrollLock", 224: "Meta" }, dc = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
  function pc(e2) {
    var n = this.nativeEvent;
    return n.getModifierState ? n.getModifierState(e2) : (e2 = dc[e2]) ? !!n[e2] : false;
  }
  function zi() {
    return pc;
  }
  var mc = F2({}, It, { key: function(e2) {
    if (e2.key) {
      var n = cc[e2.key] || e2.key;
      if (n !== "Unidentified")
        return n;
    }
    return e2.type === "keypress" ? (e2 = ur(e2), e2 === 13 ? "Enter" : String.fromCharCode(e2)) : e2.type === "keydown" || e2.type === "keyup" ? fc[e2.keyCode] || "Unidentified" : "";
  }, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: zi, charCode: function(e2) {
    return e2.type === "keypress" ? ur(e2) : 0;
  }, keyCode: function(e2) {
    return e2.type === "keydown" || e2.type === "keyup" ? e2.keyCode : 0;
  }, which: function(e2) {
    return e2.type === "keypress" ? ur(e2) : e2.type === "keydown" || e2.type === "keyup" ? e2.keyCode : 0;
  } }), hc = ce2(mc), vc = F2({}, Vr, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Eu = ce2(vc), yc = F2({}, It, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: zi }), gc = ce2(yc), wc = F2({}, Gn, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), Sc = ce2(wc), kc = F2({}, Vr, { deltaX: function(e2) {
    return "deltaX" in e2 ? e2.deltaX : "wheelDeltaX" in e2 ? -e2.wheelDeltaX : 0;
  }, deltaY: function(e2) {
    return "deltaY" in e2 ? e2.deltaY : "wheelDeltaY" in e2 ? -e2.wheelDeltaY : "wheelDelta" in e2 ? -e2.wheelDelta : 0;
  }, deltaZ: 0, deltaMode: 0 }), Ec = ce2(kc), Cc = [9, 13, 27, 32], Pi = Fe2 && "CompositionEvent" in window, ft = null;
  Fe2 && "documentMode" in document && (ft = document.documentMode);
  var xc = Fe2 && "TextEvent" in window && !ft, Yo = Fe2 && (!Pi || ft && 8 < ft && 11 >= ft), Cu = " ", xu = false;
  function Xo(e2, n) {
    switch (e2) {
      case "keyup":
        return Cc.indexOf(n.keyCode) !== -1;
      case "keydown":
        return n.keyCode !== 229;
      case "keypress":
      case "mousedown":
      case "focusout":
        return true;
      default:
        return false;
    }
  }
  function Go(e2) {
    return e2 = e2.detail, typeof e2 == "object" && "data" in e2 ? e2.data : null;
  }
  var _n = false;
  function Nc(e2, n) {
    switch (e2) {
      case "compositionend":
        return Go(n);
      case "keypress":
        return n.which !== 32 ? null : (xu = true, Cu);
      case "textInput":
        return e2 = n.data, e2 === Cu && xu ? null : e2;
      default:
        return null;
    }
  }
  function _c(e2, n) {
    if (_n)
      return e2 === "compositionend" || !Pi && Xo(e2, n) ? (e2 = Ko(), ir = Ni = Ke = null, _n = false, e2) : null;
    switch (e2) {
      case "paste":
        return null;
      case "keypress":
        if (!(n.ctrlKey || n.altKey || n.metaKey) || n.ctrlKey && n.altKey) {
          if (n.char && 1 < n.char.length)
            return n.char;
          if (n.which)
            return String.fromCharCode(n.which);
        }
        return null;
      case "compositionend":
        return Yo && n.locale !== "ko" ? null : n.data;
      default:
        return null;
    }
  }
  var zc = { color: true, date: true, datetime: true, "datetime-local": true, email: true, month: true, number: true, password: true, range: true, search: true, tel: true, text: true, time: true, url: true, week: true };
  function Nu(e2) {
    var n = e2 && e2.nodeName && e2.nodeName.toLowerCase();
    return n === "input" ? !!zc[e2.type] : n === "textarea";
  }
  function Zo(e2, n, t, r) {
    zo(r), n = kr(n, "onChange"), 0 < n.length && (t = new _i("onChange", "change", null, t, r), e2.push({ event: t, listeners: n }));
  }
  var dt = null, xt = null;
  function Pc(e2) {
    os(e2, 0);
  }
  function Ar(e2) {
    var n = Ln(e2);
    if (So(n))
      return e2;
  }
  function Lc(e2, n) {
    if (e2 === "change")
      return n;
  }
  var Jo = false;
  Fe2 && (Fe2 ? (Yt = "oninput" in document, Yt || (sl = document.createElement("div"), sl.setAttribute("oninput", "return;"), Yt = typeof sl.oninput == "function"), Kt = Yt) : Kt = false, Jo = Kt && (!document.documentMode || 9 < document.documentMode));
  var Kt, Yt, sl;
  function _u() {
    dt && (dt.detachEvent("onpropertychange", qo), xt = dt = null);
  }
  function qo(e2) {
    if (e2.propertyName === "value" && Ar(xt)) {
      var n = [];
      Zo(n, xt, e2, Si(e2)), Mo(Pc, n);
    }
  }
  function Tc(e2, n, t) {
    e2 === "focusin" ? (_u(), dt = n, xt = t, dt.attachEvent("onpropertychange", qo)) : e2 === "focusout" && _u();
  }
  function Mc(e2) {
    if (e2 === "selectionchange" || e2 === "keyup" || e2 === "keydown")
      return Ar(xt);
  }
  function Dc(e2, n) {
    if (e2 === "click")
      return Ar(n);
  }
  function Oc(e2, n) {
    if (e2 === "input" || e2 === "change")
      return Ar(n);
  }
  function Rc(e2, n) {
    return e2 === n && (e2 !== 0 || 1 / e2 === 1 / n) || e2 !== e2 && n !== n;
  }
  var xe3 = typeof Object.is == "function" ? Object.is : Rc;
  function Nt(e2, n) {
    if (xe3(e2, n))
      return true;
    if (typeof e2 != "object" || e2 === null || typeof n != "object" || n === null)
      return false;
    var t = Object.keys(e2), r = Object.keys(n);
    if (t.length !== r.length)
      return false;
    for (r = 0; r < t.length; r++) {
      var l = t[r];
      if (!El.call(n, l) || !xe3(e2[l], n[l]))
        return false;
    }
    return true;
  }
  function zu(e2) {
    for (; e2 && e2.firstChild; )
      e2 = e2.firstChild;
    return e2;
  }
  function Pu(e2, n) {
    var t = zu(e2);
    e2 = 0;
    for (var r; t; ) {
      if (t.nodeType === 3) {
        if (r = e2 + t.textContent.length, e2 <= n && r >= n)
          return { node: t, offset: n - e2 };
        e2 = r;
      }
      e: {
        for (; t; ) {
          if (t.nextSibling) {
            t = t.nextSibling;
            break e;
          }
          t = t.parentNode;
        }
        t = void 0;
      }
      t = zu(t);
    }
  }
  function bo(e2, n) {
    return e2 && n ? e2 === n ? true : e2 && e2.nodeType === 3 ? false : n && n.nodeType === 3 ? bo(e2, n.parentNode) : "contains" in e2 ? e2.contains(n) : e2.compareDocumentPosition ? !!(e2.compareDocumentPosition(n) & 16) : false : false;
  }
  function es() {
    for (var e2 = window, n = mr(); n instanceof e2.HTMLIFrameElement; ) {
      try {
        var t = typeof n.contentWindow.location.href == "string";
      } catch {
        t = false;
      }
      if (t)
        e2 = n.contentWindow;
      else
        break;
      n = mr(e2.document);
    }
    return n;
  }
  function Li(e2) {
    var n = e2 && e2.nodeName && e2.nodeName.toLowerCase();
    return n && (n === "input" && (e2.type === "text" || e2.type === "search" || e2.type === "tel" || e2.type === "url" || e2.type === "password") || n === "textarea" || e2.contentEditable === "true");
  }
  function Fc(e2) {
    var n = es(), t = e2.focusedElem, r = e2.selectionRange;
    if (n !== t && t && t.ownerDocument && bo(t.ownerDocument.documentElement, t)) {
      if (r !== null && Li(t)) {
        if (n = r.start, e2 = r.end, e2 === void 0 && (e2 = n), "selectionStart" in t)
          t.selectionStart = n, t.selectionEnd = Math.min(e2, t.value.length);
        else if (e2 = (n = t.ownerDocument || document) && n.defaultView || window, e2.getSelection) {
          e2 = e2.getSelection();
          var l = t.textContent.length, i = Math.min(r.start, l);
          r = r.end === void 0 ? i : Math.min(r.end, l), !e2.extend && i > r && (l = r, r = i, i = l), l = Pu(t, i);
          var u = Pu(t, r);
          l && u && (e2.rangeCount !== 1 || e2.anchorNode !== l.node || e2.anchorOffset !== l.offset || e2.focusNode !== u.node || e2.focusOffset !== u.offset) && (n = n.createRange(), n.setStart(l.node, l.offset), e2.removeAllRanges(), i > r ? (e2.addRange(n), e2.extend(u.node, u.offset)) : (n.setEnd(u.node, u.offset), e2.addRange(n)));
        }
      }
      for (n = [], e2 = t; e2 = e2.parentNode; )
        e2.nodeType === 1 && n.push({ element: e2, left: e2.scrollLeft, top: e2.scrollTop });
      for (typeof t.focus == "function" && t.focus(), t = 0; t < n.length; t++)
        e2 = n[t], e2.element.scrollLeft = e2.left, e2.element.scrollTop = e2.top;
    }
  }
  var Ic = Fe2 && "documentMode" in document && 11 >= document.documentMode, zn = null, Bl = null, pt = null, Hl = false;
  function Lu(e2, n, t) {
    var r = t.window === t ? t.document : t.nodeType === 9 ? t : t.ownerDocument;
    Hl || zn == null || zn !== mr(r) || (r = zn, "selectionStart" in r && Li(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), pt && Nt(pt, r) || (pt = r, r = kr(Bl, "onSelect"), 0 < r.length && (n = new _i("onSelect", "select", null, n, t), e2.push({ event: n, listeners: r }), n.target = zn)));
  }
  function Xt(e2, n) {
    var t = {};
    return t[e2.toLowerCase()] = n.toLowerCase(), t["Webkit" + e2] = "webkit" + n, t["Moz" + e2] = "moz" + n, t;
  }
  var Pn = { animationend: Xt("Animation", "AnimationEnd"), animationiteration: Xt("Animation", "AnimationIteration"), animationstart: Xt("Animation", "AnimationStart"), transitionend: Xt("Transition", "TransitionEnd") }, al = {}, ns = {};
  Fe2 && (ns = document.createElement("div").style, "AnimationEvent" in window || (delete Pn.animationend.animation, delete Pn.animationiteration.animation, delete Pn.animationstart.animation), "TransitionEvent" in window || delete Pn.transitionend.transition);
  function Br(e2) {
    if (al[e2])
      return al[e2];
    if (!Pn[e2])
      return e2;
    var n = Pn[e2], t;
    for (t in n)
      if (n.hasOwnProperty(t) && t in ns)
        return al[e2] = n[t];
    return e2;
  }
  var ts = Br("animationend"), rs = Br("animationiteration"), ls = Br("animationstart"), is = Br("transitionend"), us = new Map(), Tu = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
  function ln(e2, n) {
    us.set(e2, n), Sn(n, [e2]);
  }
  for (Gt = 0; Gt < Tu.length; Gt++)
    Zt = Tu[Gt], Mu = Zt.toLowerCase(), Du = Zt[0].toUpperCase() + Zt.slice(1), ln(Mu, "on" + Du);
  var Zt, Mu, Du, Gt;
  ln(ts, "onAnimationEnd");
  ln(rs, "onAnimationIteration");
  ln(ls, "onAnimationStart");
  ln("dblclick", "onDoubleClick");
  ln("focusin", "onFocus");
  ln("focusout", "onBlur");
  ln(is, "onTransitionEnd");
  Hn("onMouseEnter", ["mouseout", "mouseover"]);
  Hn("onMouseLeave", ["mouseout", "mouseover"]);
  Hn("onPointerEnter", ["pointerout", "pointerover"]);
  Hn("onPointerLeave", ["pointerout", "pointerover"]);
  Sn("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
  Sn("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
  Sn("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
  Sn("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
  Sn("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
  Sn("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
  var st = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), jc = new Set("cancel close invalid load scroll toggle".split(" ").concat(st));
  function Ou(e2, n, t) {
    var r = e2.type || "unknown-event";
    e2.currentTarget = t, ja(r, n, void 0, e2), e2.currentTarget = null;
  }
  function os(e2, n) {
    n = (n & 4) !== 0;
    for (var t = 0; t < e2.length; t++) {
      var r = e2[t], l = r.event;
      r = r.listeners;
      e: {
        var i = void 0;
        if (n)
          for (var u = r.length - 1; 0 <= u; u--) {
            var o = r[u], s = o.instance, d = o.currentTarget;
            if (o = o.listener, s !== i && l.isPropagationStopped())
              break e;
            Ou(l, o, d), i = s;
          }
        else
          for (u = 0; u < r.length; u++) {
            if (o = r[u], s = o.instance, d = o.currentTarget, o = o.listener, s !== i && l.isPropagationStopped())
              break e;
            Ou(l, o, d), i = s;
          }
      }
    }
    if (vr)
      throw e2 = jl, vr = false, jl = null, e2;
  }
  function T(e2, n) {
    var t = n[Yl];
    t === void 0 && (t = n[Yl] = new Set());
    var r = e2 + "__bubble";
    t.has(r) || (ss(n, e2, 2, false), t.add(r));
  }
  function cl(e2, n, t) {
    var r = 0;
    n && (r |= 4), ss(t, e2, r, n);
  }
  var Jt = "_reactListening" + Math.random().toString(36).slice(2);
  function _t(e2) {
    if (!e2[Jt]) {
      e2[Jt] = true, ho.forEach(function(t) {
        t !== "selectionchange" && (jc.has(t) || cl(t, false, e2), cl(t, true, e2));
      });
      var n = e2.nodeType === 9 ? e2 : e2.ownerDocument;
      n === null || n[Jt] || (n[Jt] = true, cl("selectionchange", false, n));
    }
  }
  function ss(e2, n, t, r) {
    switch ($o(n)) {
      case 1:
        var l = ba;
        break;
      case 4:
        l = ec;
        break;
      default:
        l = xi;
    }
    t = l.bind(null, n, t, e2), l = void 0, !Il || n !== "touchstart" && n !== "touchmove" && n !== "wheel" || (l = true), r ? l !== void 0 ? e2.addEventListener(n, t, { capture: true, passive: l }) : e2.addEventListener(n, t, true) : l !== void 0 ? e2.addEventListener(n, t, { passive: l }) : e2.addEventListener(n, t, false);
  }
  function fl(e2, n, t, r, l) {
    var i = r;
    if ((n & 1) === 0 && (n & 2) === 0 && r !== null)
      e:
        for (; ; ) {
          if (r === null)
            return;
          var u = r.tag;
          if (u === 3 || u === 4) {
            var o = r.stateNode.containerInfo;
            if (o === l || o.nodeType === 8 && o.parentNode === l)
              break;
            if (u === 4)
              for (u = r.return; u !== null; ) {
                var s = u.tag;
                if ((s === 3 || s === 4) && (s = u.stateNode.containerInfo, s === l || s.nodeType === 8 && s.parentNode === l))
                  return;
                u = u.return;
              }
            for (; o !== null; ) {
              if (u = cn(o), u === null)
                return;
              if (s = u.tag, s === 5 || s === 6) {
                r = i = u;
                continue e;
              }
              o = o.parentNode;
            }
          }
          r = r.return;
        }
    Mo(function() {
      var d = i, m = Si(t), h2 = [];
      e: {
        var p = us.get(e2);
        if (p !== void 0) {
          var g = _i, S2 = e2;
          switch (e2) {
            case "keypress":
              if (ur(t) === 0)
                break e;
            case "keydown":
            case "keyup":
              g = hc;
              break;
            case "focusin":
              S2 = "focus", g = ol;
              break;
            case "focusout":
              S2 = "blur", g = ol;
              break;
            case "beforeblur":
            case "afterblur":
              g = ol;
              break;
            case "click":
              if (t.button === 2)
                break e;
            case "auxclick":
            case "dblclick":
            case "mousedown":
            case "mousemove":
            case "mouseup":
            case "mouseout":
            case "mouseover":
            case "contextmenu":
              g = Su;
              break;
            case "drag":
            case "dragend":
            case "dragenter":
            case "dragexit":
            case "dragleave":
            case "dragover":
            case "dragstart":
            case "drop":
              g = rc;
              break;
            case "touchcancel":
            case "touchend":
            case "touchmove":
            case "touchstart":
              g = gc;
              break;
            case ts:
            case rs:
            case ls:
              g = uc;
              break;
            case is:
              g = Sc;
              break;
            case "scroll":
              g = nc;
              break;
            case "wheel":
              g = Ec;
              break;
            case "copy":
            case "cut":
            case "paste":
              g = sc;
              break;
            case "gotpointercapture":
            case "lostpointercapture":
            case "pointercancel":
            case "pointerdown":
            case "pointermove":
            case "pointerout":
            case "pointerover":
            case "pointerup":
              g = Eu;
          }
          var k2 = (n & 4) !== 0, j = !k2 && e2 === "scroll", c = k2 ? p !== null ? p + "Capture" : null : p;
          k2 = [];
          for (var a = d, f; a !== null; ) {
            f = a;
            var y = f.stateNode;
            if (f.tag === 5 && y !== null && (f = y, c !== null && (y = St(a, c), y != null && k2.push(zt(a, y, f)))), j)
              break;
            a = a.return;
          }
          0 < k2.length && (p = new g(p, S2, null, t, m), h2.push({ event: p, listeners: k2 }));
        }
      }
      if ((n & 7) === 0) {
        e: {
          if (p = e2 === "mouseover" || e2 === "pointerover", g = e2 === "mouseout" || e2 === "pointerout", p && t !== Rl && (S2 = t.relatedTarget || t.fromElement) && (cn(S2) || S2[Ie3]))
            break e;
          if ((g || p) && (p = m.window === m ? m : (p = m.ownerDocument) ? p.defaultView || p.parentWindow : window, g ? (S2 = t.relatedTarget || t.toElement, g = d, S2 = S2 ? cn(S2) : null, S2 !== null && (j = kn(S2), S2 !== j || S2.tag !== 5 && S2.tag !== 6) && (S2 = null)) : (g = null, S2 = d), g !== S2)) {
            if (k2 = Su, y = "onMouseLeave", c = "onMouseEnter", a = "mouse", (e2 === "pointerout" || e2 === "pointerover") && (k2 = Eu, y = "onPointerLeave", c = "onPointerEnter", a = "pointer"), j = g == null ? p : Ln(g), f = S2 == null ? p : Ln(S2), p = new k2(y, a + "leave", g, t, m), p.target = j, p.relatedTarget = f, y = null, cn(m) === d && (k2 = new k2(c, a + "enter", S2, t, m), k2.target = f, k2.relatedTarget = j, y = k2), j = y, g && S2)
              n: {
                for (k2 = g, c = S2, a = 0, f = k2; f; f = Cn(f))
                  a++;
                for (f = 0, y = c; y; y = Cn(y))
                  f++;
                for (; 0 < a - f; )
                  k2 = Cn(k2), a--;
                for (; 0 < f - a; )
                  c = Cn(c), f--;
                for (; a--; ) {
                  if (k2 === c || c !== null && k2 === c.alternate)
                    break n;
                  k2 = Cn(k2), c = Cn(c);
                }
                k2 = null;
              }
            else
              k2 = null;
            g !== null && Ru(h2, p, g, k2, false), S2 !== null && j !== null && Ru(h2, j, S2, k2, true);
          }
        }
        e: {
          if (p = d ? Ln(d) : window, g = p.nodeName && p.nodeName.toLowerCase(), g === "select" || g === "input" && p.type === "file")
            var E = Lc;
          else if (Nu(p))
            if (Jo)
              E = Oc;
            else {
              E = Mc;
              var C = Tc;
            }
          else
            (g = p.nodeName) && g.toLowerCase() === "input" && (p.type === "checkbox" || p.type === "radio") && (E = Dc);
          if (E && (E = E(e2, d))) {
            Zo(h2, E, t, m);
            break e;
          }
          C && C(e2, p, d), e2 === "focusout" && (C = p._wrapperState) && C.controlled && p.type === "number" && Ll(p, "number", p.value);
        }
        switch (C = d ? Ln(d) : window, e2) {
          case "focusin":
            (Nu(C) || C.contentEditable === "true") && (zn = C, Bl = d, pt = null);
            break;
          case "focusout":
            pt = Bl = zn = null;
            break;
          case "mousedown":
            Hl = true;
            break;
          case "contextmenu":
          case "mouseup":
          case "dragend":
            Hl = false, Lu(h2, t, m);
            break;
          case "selectionchange":
            if (Ic)
              break;
          case "keydown":
          case "keyup":
            Lu(h2, t, m);
        }
        var x2;
        if (Pi)
          e: {
            switch (e2) {
              case "compositionstart":
                var N2 = "onCompositionStart";
                break e;
              case "compositionend":
                N2 = "onCompositionEnd";
                break e;
              case "compositionupdate":
                N2 = "onCompositionUpdate";
                break e;
            }
            N2 = void 0;
          }
        else
          _n ? Xo(e2, t) && (N2 = "onCompositionEnd") : e2 === "keydown" && t.keyCode === 229 && (N2 = "onCompositionStart");
        N2 && (Yo && t.locale !== "ko" && (_n || N2 !== "onCompositionStart" ? N2 === "onCompositionEnd" && _n && (x2 = Ko()) : (Ke = m, Ni = "value" in Ke ? Ke.value : Ke.textContent, _n = true)), C = kr(d, N2), 0 < C.length && (N2 = new ku(N2, e2, null, t, m), h2.push({ event: N2, listeners: C }), x2 ? N2.data = x2 : (x2 = Go(t), x2 !== null && (N2.data = x2)))), (x2 = xc ? Nc(e2, t) : _c(e2, t)) && (d = kr(d, "onBeforeInput"), 0 < d.length && (m = new ku("onBeforeInput", "beforeinput", null, t, m), h2.push({ event: m, listeners: d }), m.data = x2));
      }
      os(h2, n);
    });
  }
  function zt(e2, n, t) {
    return { instance: e2, listener: n, currentTarget: t };
  }
  function kr(e2, n) {
    for (var t = n + "Capture", r = []; e2 !== null; ) {
      var l = e2, i = l.stateNode;
      l.tag === 5 && i !== null && (l = i, i = St(e2, t), i != null && r.unshift(zt(e2, i, l)), i = St(e2, n), i != null && r.push(zt(e2, i, l))), e2 = e2.return;
    }
    return r;
  }
  function Cn(e2) {
    if (e2 === null)
      return null;
    do
      e2 = e2.return;
    while (e2 && e2.tag !== 5);
    return e2 || null;
  }
  function Ru(e2, n, t, r, l) {
    for (var i = n._reactName, u = []; t !== null && t !== r; ) {
      var o = t, s = o.alternate, d = o.stateNode;
      if (s !== null && s === r)
        break;
      o.tag === 5 && d !== null && (o = d, l ? (s = St(t, i), s != null && u.unshift(zt(t, s, o))) : l || (s = St(t, i), s != null && u.push(zt(t, s, o)))), t = t.return;
    }
    u.length !== 0 && e2.push({ event: n, listeners: u });
  }
  var Uc = /\r\n?/g, Vc = /\u0000|\uFFFD/g;
  function Fu(e2) {
    return (typeof e2 == "string" ? e2 : "" + e2).replace(Uc, `
`).replace(Vc, "");
  }
  function qt(e2, n, t) {
    if (n = Fu(n), Fu(e2) !== n && t)
      throw Error(v(425));
  }
  function Er() {
  }
  var Wl = null, Ql = null;
  function $l(e2, n) {
    return e2 === "textarea" || e2 === "noscript" || typeof n.children == "string" || typeof n.children == "number" || typeof n.dangerouslySetInnerHTML == "object" && n.dangerouslySetInnerHTML !== null && n.dangerouslySetInnerHTML.__html != null;
  }
  var Kl = typeof setTimeout == "function" ? setTimeout : void 0, Ac = typeof clearTimeout == "function" ? clearTimeout : void 0, Iu = typeof Promise == "function" ? Promise : void 0, Bc = typeof queueMicrotask == "function" ? queueMicrotask : typeof Iu < "u" ? function(e2) {
    return Iu.resolve(null).then(e2).catch(Hc);
  } : Kl;
  function Hc(e2) {
    setTimeout(function() {
      throw e2;
    });
  }
  function dl(e2, n) {
    var t = n, r = 0;
    do {
      var l = t.nextSibling;
      if (e2.removeChild(t), l && l.nodeType === 8)
        if (t = l.data, t === "/$") {
          if (r === 0) {
            e2.removeChild(l), Ct(n);
            return;
          }
          r--;
        } else
          t !== "$" && t !== "$?" && t !== "$!" || r++;
      t = l;
    } while (t);
    Ct(n);
  }
  function Je(e2) {
    for (; e2 != null; e2 = e2.nextSibling) {
      var n = e2.nodeType;
      if (n === 1 || n === 3)
        break;
      if (n === 8) {
        if (n = e2.data, n === "$" || n === "$!" || n === "$?")
          break;
        if (n === "/$")
          return null;
      }
    }
    return e2;
  }
  function ju(e2) {
    e2 = e2.previousSibling;
    for (var n = 0; e2; ) {
      if (e2.nodeType === 8) {
        var t = e2.data;
        if (t === "$" || t === "$!" || t === "$?") {
          if (n === 0)
            return e2;
          n--;
        } else
          t === "/$" && n++;
      }
      e2 = e2.previousSibling;
    }
    return null;
  }
  var Zn = Math.random().toString(36).slice(2), ze2 = "__reactFiber$" + Zn, Pt = "__reactProps$" + Zn, Ie3 = "__reactContainer$" + Zn, Yl = "__reactEvents$" + Zn, Wc = "__reactListeners$" + Zn, Qc = "__reactHandles$" + Zn;
  function cn(e2) {
    var n = e2[ze2];
    if (n)
      return n;
    for (var t = e2.parentNode; t; ) {
      if (n = t[Ie3] || t[ze2]) {
        if (t = n.alternate, n.child !== null || t !== null && t.child !== null)
          for (e2 = ju(e2); e2 !== null; ) {
            if (t = e2[ze2])
              return t;
            e2 = ju(e2);
          }
        return n;
      }
      e2 = t, t = e2.parentNode;
    }
    return null;
  }
  function jt(e2) {
    return e2 = e2[ze2] || e2[Ie3], !e2 || e2.tag !== 5 && e2.tag !== 6 && e2.tag !== 13 && e2.tag !== 3 ? null : e2;
  }
  function Ln(e2) {
    if (e2.tag === 5 || e2.tag === 6)
      return e2.stateNode;
    throw Error(v(33));
  }
  function Hr(e2) {
    return e2[Pt] || null;
  }
  var Xl = [], Tn = -1;
  function un(e2) {
    return { current: e2 };
  }
  function M2(e2) {
    0 > Tn || (e2.current = Xl[Tn], Xl[Tn] = null, Tn--);
  }
  function L(e2, n) {
    Tn++, Xl[Tn] = e2.current, e2.current = n;
  }
  var rn = {}, J = un(rn), re = un(false), hn = rn;
  function Wn(e2, n) {
    var t = e2.type.contextTypes;
    if (!t)
      return rn;
    var r = e2.stateNode;
    if (r && r.__reactInternalMemoizedUnmaskedChildContext === n)
      return r.__reactInternalMemoizedMaskedChildContext;
    var l = {}, i;
    for (i in t)
      l[i] = n[i];
    return r && (e2 = e2.stateNode, e2.__reactInternalMemoizedUnmaskedChildContext = n, e2.__reactInternalMemoizedMaskedChildContext = l), l;
  }
  function le2(e2) {
    return e2 = e2.childContextTypes, e2 != null;
  }
  function Cr() {
    M2(re), M2(J);
  }
  function Uu(e2, n, t) {
    if (J.current !== rn)
      throw Error(v(168));
    L(J, n), L(re, t);
  }
  function as(e2, n, t) {
    var r = e2.stateNode;
    if (n = n.childContextTypes, typeof r.getChildContext != "function")
      return t;
    r = r.getChildContext();
    for (var l in r)
      if (!(l in n))
        throw Error(v(108, Ta(e2) || "Unknown", l));
    return F2({}, t, r);
  }
  function xr(e2) {
    return e2 = (e2 = e2.stateNode) && e2.__reactInternalMemoizedMergedChildContext || rn, hn = J.current, L(J, e2), L(re, re.current), true;
  }
  function Vu(e2, n, t) {
    var r = e2.stateNode;
    if (!r)
      throw Error(v(169));
    t ? (e2 = as(e2, n, hn), r.__reactInternalMemoizedMergedChildContext = e2, M2(re), M2(J), L(J, e2)) : M2(re), L(re, t);
  }
  var Me2 = null, Wr = false, pl = false;
  function cs(e2) {
    Me2 === null ? Me2 = [e2] : Me2.push(e2);
  }
  function $c(e2) {
    Wr = true, cs(e2);
  }
  function on() {
    if (!pl && Me2 !== null) {
      pl = true;
      var e2 = 0, n = P;
      try {
        var t = Me2;
        for (P = 1; e2 < t.length; e2++) {
          var r = t[e2];
          do
            r = r(true);
          while (r !== null);
        }
        Me2 = null, Wr = false;
      } catch (l) {
        throw Me2 !== null && (Me2 = Me2.slice(e2 + 1)), Fo(ki, on), l;
      } finally {
        P = n, pl = false;
      }
    }
    return null;
  }
  var Mn = [], Dn = 0, Nr = null, _r = 0, de3 = [], pe3 = 0, vn = null, De2 = 1, Oe2 = "";
  function sn(e2, n) {
    Mn[Dn++] = _r, Mn[Dn++] = Nr, Nr = e2, _r = n;
  }
  function fs(e2, n, t) {
    de3[pe3++] = De2, de3[pe3++] = Oe2, de3[pe3++] = vn, vn = e2;
    var r = De2;
    e2 = Oe2;
    var l = 32 - Ee2(r) - 1;
    r &= ~(1 << l), t += 1;
    var i = 32 - Ee2(n) + l;
    if (30 < i) {
      var u = l - l % 5;
      i = (r & (1 << u) - 1).toString(32), r >>= u, l -= u, De2 = 1 << 32 - Ee2(n) + l | t << l | r, Oe2 = i + e2;
    } else
      De2 = 1 << i | t << l | r, Oe2 = e2;
  }
  function Ti(e2) {
    e2.return !== null && (sn(e2, 1), fs(e2, 1, 0));
  }
  function Mi(e2) {
    for (; e2 === Nr; )
      Nr = Mn[--Dn], Mn[Dn] = null, _r = Mn[--Dn], Mn[Dn] = null;
    for (; e2 === vn; )
      vn = de3[--pe3], de3[pe3] = null, Oe2 = de3[--pe3], de3[pe3] = null, De2 = de3[--pe3], de3[pe3] = null;
  }
  var se2 = null, oe2 = null, D2 = false, ke3 = null;
  function ds(e2, n) {
    var t = me3(5, null, null, 0);
    t.elementType = "DELETED", t.stateNode = n, t.return = e2, n = e2.deletions, n === null ? (e2.deletions = [t], e2.flags |= 16) : n.push(t);
  }
  function Au(e2, n) {
    switch (e2.tag) {
      case 5:
        var t = e2.type;
        return n = n.nodeType !== 1 || t.toLowerCase() !== n.nodeName.toLowerCase() ? null : n, n !== null ? (e2.stateNode = n, se2 = e2, oe2 = Je(n.firstChild), true) : false;
      case 6:
        return n = e2.pendingProps === "" || n.nodeType !== 3 ? null : n, n !== null ? (e2.stateNode = n, se2 = e2, oe2 = null, true) : false;
      case 13:
        return n = n.nodeType !== 8 ? null : n, n !== null ? (t = vn !== null ? { id: De2, overflow: Oe2 } : null, e2.memoizedState = { dehydrated: n, treeContext: t, retryLane: 1073741824 }, t = me3(18, null, null, 0), t.stateNode = n, t.return = e2, e2.child = t, se2 = e2, oe2 = null, true) : false;
      default:
        return false;
    }
  }
  function Gl(e2) {
    return (e2.mode & 1) !== 0 && (e2.flags & 128) === 0;
  }
  function Zl(e2) {
    if (D2) {
      var n = oe2;
      if (n) {
        var t = n;
        if (!Au(e2, n)) {
          if (Gl(e2))
            throw Error(v(418));
          n = Je(t.nextSibling);
          var r = se2;
          n && Au(e2, n) ? ds(r, t) : (e2.flags = e2.flags & -4097 | 2, D2 = false, se2 = e2);
        }
      } else {
        if (Gl(e2))
          throw Error(v(418));
        e2.flags = e2.flags & -4097 | 2, D2 = false, se2 = e2;
      }
    }
  }
  function Bu(e2) {
    for (e2 = e2.return; e2 !== null && e2.tag !== 5 && e2.tag !== 3 && e2.tag !== 13; )
      e2 = e2.return;
    se2 = e2;
  }
  function bt(e2) {
    if (e2 !== se2)
      return false;
    if (!D2)
      return Bu(e2), D2 = true, false;
    var n;
    if ((n = e2.tag !== 3) && !(n = e2.tag !== 5) && (n = e2.type, n = n !== "head" && n !== "body" && !$l(e2.type, e2.memoizedProps)), n && (n = oe2)) {
      if (Gl(e2))
        throw ps(), Error(v(418));
      for (; n; )
        ds(e2, n), n = Je(n.nextSibling);
    }
    if (Bu(e2), e2.tag === 13) {
      if (e2 = e2.memoizedState, e2 = e2 !== null ? e2.dehydrated : null, !e2)
        throw Error(v(317));
      e: {
        for (e2 = e2.nextSibling, n = 0; e2; ) {
          if (e2.nodeType === 8) {
            var t = e2.data;
            if (t === "/$") {
              if (n === 0) {
                oe2 = Je(e2.nextSibling);
                break e;
              }
              n--;
            } else
              t !== "$" && t !== "$!" && t !== "$?" || n++;
          }
          e2 = e2.nextSibling;
        }
        oe2 = null;
      }
    } else
      oe2 = se2 ? Je(e2.stateNode.nextSibling) : null;
    return true;
  }
  function ps() {
    for (var e2 = oe2; e2; )
      e2 = Je(e2.nextSibling);
  }
  function Qn() {
    oe2 = se2 = null, D2 = false;
  }
  function Di(e2) {
    ke3 === null ? ke3 = [e2] : ke3.push(e2);
  }
  var Kc = Ve2.ReactCurrentBatchConfig;
  function we3(e2, n) {
    if (e2 && e2.defaultProps) {
      n = F2({}, n), e2 = e2.defaultProps;
      for (var t in e2)
        n[t] === void 0 && (n[t] = e2[t]);
      return n;
    }
    return n;
  }
  var zr = un(null), Pr = null, On = null, Oi = null;
  function Ri() {
    Oi = On = Pr = null;
  }
  function Fi(e2) {
    var n = zr.current;
    M2(zr), e2._currentValue = n;
  }
  function Jl(e2, n, t) {
    for (; e2 !== null; ) {
      var r = e2.alternate;
      if ((e2.childLanes & n) !== n ? (e2.childLanes |= n, r !== null && (r.childLanes |= n)) : r !== null && (r.childLanes & n) !== n && (r.childLanes |= n), e2 === t)
        break;
      e2 = e2.return;
    }
  }
  function An(e2, n) {
    Pr = e2, Oi = On = null, e2 = e2.dependencies, e2 !== null && e2.firstContext !== null && ((e2.lanes & n) !== 0 && (te = true), e2.firstContext = null);
  }
  function ve3(e2) {
    var n = e2._currentValue;
    if (Oi !== e2)
      if (e2 = { context: e2, memoizedValue: n, next: null }, On === null) {
        if (Pr === null)
          throw Error(v(308));
        On = e2, Pr.dependencies = { lanes: 0, firstContext: e2 };
      } else
        On = On.next = e2;
    return n;
  }
  var fn = null;
  function Ii(e2) {
    fn === null ? fn = [e2] : fn.push(e2);
  }
  function ms(e2, n, t, r) {
    var l = n.interleaved;
    return l === null ? (t.next = t, Ii(n)) : (t.next = l.next, l.next = t), n.interleaved = t, je2(e2, r);
  }
  function je2(e2, n) {
    e2.lanes |= n;
    var t = e2.alternate;
    for (t !== null && (t.lanes |= n), t = e2, e2 = e2.return; e2 !== null; )
      e2.childLanes |= n, t = e2.alternate, t !== null && (t.childLanes |= n), t = e2, e2 = e2.return;
    return t.tag === 3 ? t.stateNode : null;
  }
  var We = false;
  function ji(e2) {
    e2.updateQueue = { baseState: e2.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
  }
  function hs(e2, n) {
    e2 = e2.updateQueue, n.updateQueue === e2 && (n.updateQueue = { baseState: e2.baseState, firstBaseUpdate: e2.firstBaseUpdate, lastBaseUpdate: e2.lastBaseUpdate, shared: e2.shared, effects: e2.effects });
  }
  function Re2(e2, n) {
    return { eventTime: e2, lane: n, tag: 0, payload: null, callback: null, next: null };
  }
  function qe2(e2, n, t) {
    var r = e2.updateQueue;
    if (r === null)
      return null;
    if (r = r.shared, (_ & 2) !== 0) {
      var l = r.pending;
      return l === null ? n.next = n : (n.next = l.next, l.next = n), r.pending = n, je2(e2, t);
    }
    return l = r.interleaved, l === null ? (n.next = n, Ii(r)) : (n.next = l.next, l.next = n), r.interleaved = n, je2(e2, t);
  }
  function or(e2, n, t) {
    if (n = n.updateQueue, n !== null && (n = n.shared, (t & 4194240) !== 0)) {
      var r = n.lanes;
      r &= e2.pendingLanes, t |= r, n.lanes = t, Ei(e2, t);
    }
  }
  function Hu(e2, n) {
    var t = e2.updateQueue, r = e2.alternate;
    if (r !== null && (r = r.updateQueue, t === r)) {
      var l = null, i = null;
      if (t = t.firstBaseUpdate, t !== null) {
        do {
          var u = { eventTime: t.eventTime, lane: t.lane, tag: t.tag, payload: t.payload, callback: t.callback, next: null };
          i === null ? l = i = u : i = i.next = u, t = t.next;
        } while (t !== null);
        i === null ? l = i = n : i = i.next = n;
      } else
        l = i = n;
      t = { baseState: r.baseState, firstBaseUpdate: l, lastBaseUpdate: i, shared: r.shared, effects: r.effects }, e2.updateQueue = t;
      return;
    }
    e2 = t.lastBaseUpdate, e2 === null ? t.firstBaseUpdate = n : e2.next = n, t.lastBaseUpdate = n;
  }
  function Lr(e2, n, t, r) {
    var l = e2.updateQueue;
    We = false;
    var i = l.firstBaseUpdate, u = l.lastBaseUpdate, o = l.shared.pending;
    if (o !== null) {
      l.shared.pending = null;
      var s = o, d = s.next;
      s.next = null, u === null ? i = d : u.next = d, u = s;
      var m = e2.alternate;
      m !== null && (m = m.updateQueue, o = m.lastBaseUpdate, o !== u && (o === null ? m.firstBaseUpdate = d : o.next = d, m.lastBaseUpdate = s));
    }
    if (i !== null) {
      var h2 = l.baseState;
      u = 0, m = d = s = null, o = i;
      do {
        var p = o.lane, g = o.eventTime;
        if ((r & p) === p) {
          m !== null && (m = m.next = { eventTime: g, lane: 0, tag: o.tag, payload: o.payload, callback: o.callback, next: null });
          e: {
            var S2 = e2, k2 = o;
            switch (p = n, g = t, k2.tag) {
              case 1:
                if (S2 = k2.payload, typeof S2 == "function") {
                  h2 = S2.call(g, h2, p);
                  break e;
                }
                h2 = S2;
                break e;
              case 3:
                S2.flags = S2.flags & -65537 | 128;
              case 0:
                if (S2 = k2.payload, p = typeof S2 == "function" ? S2.call(g, h2, p) : S2, p == null)
                  break e;
                h2 = F2({}, h2, p);
                break e;
              case 2:
                We = true;
            }
          }
          o.callback !== null && o.lane !== 0 && (e2.flags |= 64, p = l.effects, p === null ? l.effects = [o] : p.push(o));
        } else
          g = { eventTime: g, lane: p, tag: o.tag, payload: o.payload, callback: o.callback, next: null }, m === null ? (d = m = g, s = h2) : m = m.next = g, u |= p;
        if (o = o.next, o === null) {
          if (o = l.shared.pending, o === null)
            break;
          p = o, o = p.next, p.next = null, l.lastBaseUpdate = p, l.shared.pending = null;
        }
      } while (true);
      if (m === null && (s = h2), l.baseState = s, l.firstBaseUpdate = d, l.lastBaseUpdate = m, n = l.shared.interleaved, n !== null) {
        l = n;
        do
          u |= l.lane, l = l.next;
        while (l !== n);
      } else
        i === null && (l.shared.lanes = 0);
      gn |= u, e2.lanes = u, e2.memoizedState = h2;
    }
  }
  function Wu(e2, n, t) {
    if (e2 = n.effects, n.effects = null, e2 !== null)
      for (n = 0; n < e2.length; n++) {
        var r = e2[n], l = r.callback;
        if (l !== null) {
          if (r.callback = null, r = t, typeof l != "function")
            throw Error(v(191, l));
          l.call(r);
        }
      }
  }
  var vs = new mo.Component().refs;
  function ql(e2, n, t, r) {
    n = e2.memoizedState, t = t(r, n), t = t == null ? n : F2({}, n, t), e2.memoizedState = t, e2.lanes === 0 && (e2.updateQueue.baseState = t);
  }
  var Qr = { isMounted: function(e2) {
    return (e2 = e2._reactInternals) ? kn(e2) === e2 : false;
  }, enqueueSetState: function(e2, n, t) {
    e2 = e2._reactInternals;
    var r = b(), l = en(e2), i = Re2(r, l);
    i.payload = n, t != null && (i.callback = t), n = qe2(e2, i, l), n !== null && (Ce2(n, e2, l, r), or(n, e2, l));
  }, enqueueReplaceState: function(e2, n, t) {
    e2 = e2._reactInternals;
    var r = b(), l = en(e2), i = Re2(r, l);
    i.tag = 1, i.payload = n, t != null && (i.callback = t), n = qe2(e2, i, l), n !== null && (Ce2(n, e2, l, r), or(n, e2, l));
  }, enqueueForceUpdate: function(e2, n) {
    e2 = e2._reactInternals;
    var t = b(), r = en(e2), l = Re2(t, r);
    l.tag = 2, n != null && (l.callback = n), n = qe2(e2, l, r), n !== null && (Ce2(n, e2, r, t), or(n, e2, r));
  } };
  function Qu(e2, n, t, r, l, i, u) {
    return e2 = e2.stateNode, typeof e2.shouldComponentUpdate == "function" ? e2.shouldComponentUpdate(r, i, u) : n.prototype && n.prototype.isPureReactComponent ? !Nt(t, r) || !Nt(l, i) : true;
  }
  function ys(e2, n, t) {
    var r = false, l = rn, i = n.contextType;
    return typeof i == "object" && i !== null ? i = ve3(i) : (l = le2(n) ? hn : J.current, r = n.contextTypes, i = (r = r != null) ? Wn(e2, l) : rn), n = new n(t, i), e2.memoizedState = n.state !== null && n.state !== void 0 ? n.state : null, n.updater = Qr, e2.stateNode = n, n._reactInternals = e2, r && (e2 = e2.stateNode, e2.__reactInternalMemoizedUnmaskedChildContext = l, e2.__reactInternalMemoizedMaskedChildContext = i), n;
  }
  function $u(e2, n, t, r) {
    e2 = n.state, typeof n.componentWillReceiveProps == "function" && n.componentWillReceiveProps(t, r), typeof n.UNSAFE_componentWillReceiveProps == "function" && n.UNSAFE_componentWillReceiveProps(t, r), n.state !== e2 && Qr.enqueueReplaceState(n, n.state, null);
  }
  function bl(e2, n, t, r) {
    var l = e2.stateNode;
    l.props = t, l.state = e2.memoizedState, l.refs = vs, ji(e2);
    var i = n.contextType;
    typeof i == "object" && i !== null ? l.context = ve3(i) : (i = le2(n) ? hn : J.current, l.context = Wn(e2, i)), l.state = e2.memoizedState, i = n.getDerivedStateFromProps, typeof i == "function" && (ql(e2, n, i, t), l.state = e2.memoizedState), typeof n.getDerivedStateFromProps == "function" || typeof l.getSnapshotBeforeUpdate == "function" || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (n = l.state, typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount(), n !== l.state && Qr.enqueueReplaceState(l, l.state, null), Lr(e2, t, l, r), l.state = e2.memoizedState), typeof l.componentDidMount == "function" && (e2.flags |= 4194308);
  }
  function nt(e2, n, t) {
    if (e2 = t.ref, e2 !== null && typeof e2 != "function" && typeof e2 != "object") {
      if (t._owner) {
        if (t = t._owner, t) {
          if (t.tag !== 1)
            throw Error(v(309));
          var r = t.stateNode;
        }
        if (!r)
          throw Error(v(147, e2));
        var l = r, i = "" + e2;
        return n !== null && n.ref !== null && typeof n.ref == "function" && n.ref._stringRef === i ? n.ref : (n = function(u) {
          var o = l.refs;
          o === vs && (o = l.refs = {}), u === null ? delete o[i] : o[i] = u;
        }, n._stringRef = i, n);
      }
      if (typeof e2 != "string")
        throw Error(v(284));
      if (!t._owner)
        throw Error(v(290, e2));
    }
    return e2;
  }
  function er(e2, n) {
    throw e2 = Object.prototype.toString.call(n), Error(v(31, e2 === "[object Object]" ? "object with keys {" + Object.keys(n).join(", ") + "}" : e2));
  }
  function Ku(e2) {
    var n = e2._init;
    return n(e2._payload);
  }
  function gs(e2) {
    function n(c, a) {
      if (e2) {
        var f = c.deletions;
        f === null ? (c.deletions = [a], c.flags |= 16) : f.push(a);
      }
    }
    function t(c, a) {
      if (!e2)
        return null;
      for (; a !== null; )
        n(c, a), a = a.sibling;
      return null;
    }
    function r(c, a) {
      for (c = new Map(); a !== null; )
        a.key !== null ? c.set(a.key, a) : c.set(a.index, a), a = a.sibling;
      return c;
    }
    function l(c, a) {
      return c = nn(c, a), c.index = 0, c.sibling = null, c;
    }
    function i(c, a, f) {
      return c.index = f, e2 ? (f = c.alternate, f !== null ? (f = f.index, f < a ? (c.flags |= 2, a) : f) : (c.flags |= 2, a)) : (c.flags |= 1048576, a);
    }
    function u(c) {
      return e2 && c.alternate === null && (c.flags |= 2), c;
    }
    function o(c, a, f, y) {
      return a === null || a.tag !== 6 ? (a = Sl(f, c.mode, y), a.return = c, a) : (a = l(a, f), a.return = c, a);
    }
    function s(c, a, f, y) {
      var E = f.type;
      return E === Nn ? m(c, a, f.props.children, y, f.key) : a !== null && (a.elementType === E || typeof E == "object" && E !== null && E.$$typeof === He && Ku(E) === a.type) ? (y = l(a, f.props), y.ref = nt(c, a, f), y.return = c, y) : (y = pr(f.type, f.key, f.props, null, c.mode, y), y.ref = nt(c, a, f), y.return = c, y);
    }
    function d(c, a, f, y) {
      return a === null || a.tag !== 4 || a.stateNode.containerInfo !== f.containerInfo || a.stateNode.implementation !== f.implementation ? (a = kl(f, c.mode, y), a.return = c, a) : (a = l(a, f.children || []), a.return = c, a);
    }
    function m(c, a, f, y, E) {
      return a === null || a.tag !== 7 ? (a = mn(f, c.mode, y, E), a.return = c, a) : (a = l(a, f), a.return = c, a);
    }
    function h2(c, a, f) {
      if (typeof a == "string" && a !== "" || typeof a == "number")
        return a = Sl("" + a, c.mode, f), a.return = c, a;
      if (typeof a == "object" && a !== null) {
        switch (a.$$typeof) {
          case Vt:
            return f = pr(a.type, a.key, a.props, null, c.mode, f), f.ref = nt(c, null, a), f.return = c, f;
          case xn:
            return a = kl(a, c.mode, f), a.return = c, a;
          case He:
            var y = a._init;
            return h2(c, y(a._payload), f);
        }
        if (ut(a) || Jn(a))
          return a = mn(a, c.mode, f, null), a.return = c, a;
        er(c, a);
      }
      return null;
    }
    function p(c, a, f, y) {
      var E = a !== null ? a.key : null;
      if (typeof f == "string" && f !== "" || typeof f == "number")
        return E !== null ? null : o(c, a, "" + f, y);
      if (typeof f == "object" && f !== null) {
        switch (f.$$typeof) {
          case Vt:
            return f.key === E ? s(c, a, f, y) : null;
          case xn:
            return f.key === E ? d(c, a, f, y) : null;
          case He:
            return E = f._init, p(c, a, E(f._payload), y);
        }
        if (ut(f) || Jn(f))
          return E !== null ? null : m(c, a, f, y, null);
        er(c, f);
      }
      return null;
    }
    function g(c, a, f, y, E) {
      if (typeof y == "string" && y !== "" || typeof y == "number")
        return c = c.get(f) || null, o(a, c, "" + y, E);
      if (typeof y == "object" && y !== null) {
        switch (y.$$typeof) {
          case Vt:
            return c = c.get(y.key === null ? f : y.key) || null, s(a, c, y, E);
          case xn:
            return c = c.get(y.key === null ? f : y.key) || null, d(a, c, y, E);
          case He:
            var C = y._init;
            return g(c, a, f, C(y._payload), E);
        }
        if (ut(y) || Jn(y))
          return c = c.get(f) || null, m(a, c, y, E, null);
        er(a, y);
      }
      return null;
    }
    function S2(c, a, f, y) {
      for (var E = null, C = null, x2 = a, N2 = a = 0, H = null; x2 !== null && N2 < f.length; N2++) {
        x2.index > N2 ? (H = x2, x2 = null) : H = x2.sibling;
        var z2 = p(c, x2, f[N2], y);
        if (z2 === null) {
          x2 === null && (x2 = H);
          break;
        }
        e2 && x2 && z2.alternate === null && n(c, x2), a = i(z2, a, N2), C === null ? E = z2 : C.sibling = z2, C = z2, x2 = H;
      }
      if (N2 === f.length)
        return t(c, x2), D2 && sn(c, N2), E;
      if (x2 === null) {
        for (; N2 < f.length; N2++)
          x2 = h2(c, f[N2], y), x2 !== null && (a = i(x2, a, N2), C === null ? E = x2 : C.sibling = x2, C = x2);
        return D2 && sn(c, N2), E;
      }
      for (x2 = r(c, x2); N2 < f.length; N2++)
        H = g(x2, c, N2, f[N2], y), H !== null && (e2 && H.alternate !== null && x2.delete(H.key === null ? N2 : H.key), a = i(H, a, N2), C === null ? E = H : C.sibling = H, C = H);
      return e2 && x2.forEach(function(Ae2) {
        return n(c, Ae2);
      }), D2 && sn(c, N2), E;
    }
    function k2(c, a, f, y) {
      var E = Jn(f);
      if (typeof E != "function")
        throw Error(v(150));
      if (f = E.call(f), f == null)
        throw Error(v(151));
      for (var C = E = null, x2 = a, N2 = a = 0, H = null, z2 = f.next(); x2 !== null && !z2.done; N2++, z2 = f.next()) {
        x2.index > N2 ? (H = x2, x2 = null) : H = x2.sibling;
        var Ae2 = p(c, x2, z2.value, y);
        if (Ae2 === null) {
          x2 === null && (x2 = H);
          break;
        }
        e2 && x2 && Ae2.alternate === null && n(c, x2), a = i(Ae2, a, N2), C === null ? E = Ae2 : C.sibling = Ae2, C = Ae2, x2 = H;
      }
      if (z2.done)
        return t(c, x2), D2 && sn(c, N2), E;
      if (x2 === null) {
        for (; !z2.done; N2++, z2 = f.next())
          z2 = h2(c, z2.value, y), z2 !== null && (a = i(z2, a, N2), C === null ? E = z2 : C.sibling = z2, C = z2);
        return D2 && sn(c, N2), E;
      }
      for (x2 = r(c, x2); !z2.done; N2++, z2 = f.next())
        z2 = g(x2, c, N2, z2.value, y), z2 !== null && (e2 && z2.alternate !== null && x2.delete(z2.key === null ? N2 : z2.key), a = i(z2, a, N2), C === null ? E = z2 : C.sibling = z2, C = z2);
      return e2 && x2.forEach(function(ya) {
        return n(c, ya);
      }), D2 && sn(c, N2), E;
    }
    function j(c, a, f, y) {
      if (typeof f == "object" && f !== null && f.type === Nn && f.key === null && (f = f.props.children), typeof f == "object" && f !== null) {
        switch (f.$$typeof) {
          case Vt:
            e: {
              for (var E = f.key, C = a; C !== null; ) {
                if (C.key === E) {
                  if (E = f.type, E === Nn) {
                    if (C.tag === 7) {
                      t(c, C.sibling), a = l(C, f.props.children), a.return = c, c = a;
                      break e;
                    }
                  } else if (C.elementType === E || typeof E == "object" && E !== null && E.$$typeof === He && Ku(E) === C.type) {
                    t(c, C.sibling), a = l(C, f.props), a.ref = nt(c, C, f), a.return = c, c = a;
                    break e;
                  }
                  t(c, C);
                  break;
                } else
                  n(c, C);
                C = C.sibling;
              }
              f.type === Nn ? (a = mn(f.props.children, c.mode, y, f.key), a.return = c, c = a) : (y = pr(f.type, f.key, f.props, null, c.mode, y), y.ref = nt(c, a, f), y.return = c, c = y);
            }
            return u(c);
          case xn:
            e: {
              for (C = f.key; a !== null; ) {
                if (a.key === C)
                  if (a.tag === 4 && a.stateNode.containerInfo === f.containerInfo && a.stateNode.implementation === f.implementation) {
                    t(c, a.sibling), a = l(a, f.children || []), a.return = c, c = a;
                    break e;
                  } else {
                    t(c, a);
                    break;
                  }
                else
                  n(c, a);
                a = a.sibling;
              }
              a = kl(f, c.mode, y), a.return = c, c = a;
            }
            return u(c);
          case He:
            return C = f._init, j(c, a, C(f._payload), y);
        }
        if (ut(f))
          return S2(c, a, f, y);
        if (Jn(f))
          return k2(c, a, f, y);
        er(c, f);
      }
      return typeof f == "string" && f !== "" || typeof f == "number" ? (f = "" + f, a !== null && a.tag === 6 ? (t(c, a.sibling), a = l(a, f), a.return = c, c = a) : (t(c, a), a = Sl(f, c.mode, y), a.return = c, c = a), u(c)) : t(c, a);
    }
    return j;
  }
  var $n = gs(true), ws = gs(false), Ut = {}, Le2 = un(Ut), Lt = un(Ut), Tt = un(Ut);
  function dn(e2) {
    if (e2 === Ut)
      throw Error(v(174));
    return e2;
  }
  function Ui(e2, n) {
    switch (L(Tt, n), L(Lt, e2), L(Le2, Ut), e2 = n.nodeType, e2) {
      case 9:
      case 11:
        n = (n = n.documentElement) ? n.namespaceURI : Ml(null, "");
        break;
      default:
        e2 = e2 === 8 ? n.parentNode : n, n = e2.namespaceURI || null, e2 = e2.tagName, n = Ml(n, e2);
    }
    M2(Le2), L(Le2, n);
  }
  function Kn() {
    M2(Le2), M2(Lt), M2(Tt);
  }
  function Ss(e2) {
    dn(Tt.current);
    var n = dn(Le2.current), t = Ml(n, e2.type);
    n !== t && (L(Lt, e2), L(Le2, t));
  }
  function Vi(e2) {
    Lt.current === e2 && (M2(Le2), M2(Lt));
  }
  var O = un(0);
  function Tr(e2) {
    for (var n = e2; n !== null; ) {
      if (n.tag === 13) {
        var t = n.memoizedState;
        if (t !== null && (t = t.dehydrated, t === null || t.data === "$?" || t.data === "$!"))
          return n;
      } else if (n.tag === 19 && n.memoizedProps.revealOrder !== void 0) {
        if ((n.flags & 128) !== 0)
          return n;
      } else if (n.child !== null) {
        n.child.return = n, n = n.child;
        continue;
      }
      if (n === e2)
        break;
      for (; n.sibling === null; ) {
        if (n.return === null || n.return === e2)
          return null;
        n = n.return;
      }
      n.sibling.return = n.return, n = n.sibling;
    }
    return null;
  }
  var ml = [];
  function Ai() {
    for (var e2 = 0; e2 < ml.length; e2++)
      ml[e2]._workInProgressVersionPrimary = null;
    ml.length = 0;
  }
  var sr = Ve2.ReactCurrentDispatcher, hl = Ve2.ReactCurrentBatchConfig, yn = 0, R = null, A2 = null, W = null, Mr = false, mt = false, Mt = 0, Yc = 0;
  function X2() {
    throw Error(v(321));
  }
  function Bi(e2, n) {
    if (n === null)
      return false;
    for (var t = 0; t < n.length && t < e2.length; t++)
      if (!xe3(e2[t], n[t]))
        return false;
    return true;
  }
  function Hi(e2, n, t, r, l, i) {
    if (yn = i, R = n, n.memoizedState = null, n.updateQueue = null, n.lanes = 0, sr.current = e2 === null || e2.memoizedState === null ? Jc : qc, e2 = t(r, l), mt) {
      i = 0;
      do {
        if (mt = false, Mt = 0, 25 <= i)
          throw Error(v(301));
        i += 1, W = A2 = null, n.updateQueue = null, sr.current = bc, e2 = t(r, l);
      } while (mt);
    }
    if (sr.current = Dr, n = A2 !== null && A2.next !== null, yn = 0, W = A2 = R = null, Mr = false, n)
      throw Error(v(300));
    return e2;
  }
  function Wi() {
    var e2 = Mt !== 0;
    return Mt = 0, e2;
  }
  function _e3() {
    var e2 = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
    return W === null ? R.memoizedState = W = e2 : W = W.next = e2, W;
  }
  function ye3() {
    if (A2 === null) {
      var e2 = R.alternate;
      e2 = e2 !== null ? e2.memoizedState : null;
    } else
      e2 = A2.next;
    var n = W === null ? R.memoizedState : W.next;
    if (n !== null)
      W = n, A2 = e2;
    else {
      if (e2 === null)
        throw Error(v(310));
      A2 = e2, e2 = { memoizedState: A2.memoizedState, baseState: A2.baseState, baseQueue: A2.baseQueue, queue: A2.queue, next: null }, W === null ? R.memoizedState = W = e2 : W = W.next = e2;
    }
    return W;
  }
  function Dt(e2, n) {
    return typeof n == "function" ? n(e2) : n;
  }
  function vl(e2) {
    var n = ye3(), t = n.queue;
    if (t === null)
      throw Error(v(311));
    t.lastRenderedReducer = e2;
    var r = A2, l = r.baseQueue, i = t.pending;
    if (i !== null) {
      if (l !== null) {
        var u = l.next;
        l.next = i.next, i.next = u;
      }
      r.baseQueue = l = i, t.pending = null;
    }
    if (l !== null) {
      i = l.next, r = r.baseState;
      var o = u = null, s = null, d = i;
      do {
        var m = d.lane;
        if ((yn & m) === m)
          s !== null && (s = s.next = { lane: 0, action: d.action, hasEagerState: d.hasEagerState, eagerState: d.eagerState, next: null }), r = d.hasEagerState ? d.eagerState : e2(r, d.action);
        else {
          var h2 = { lane: m, action: d.action, hasEagerState: d.hasEagerState, eagerState: d.eagerState, next: null };
          s === null ? (o = s = h2, u = r) : s = s.next = h2, R.lanes |= m, gn |= m;
        }
        d = d.next;
      } while (d !== null && d !== i);
      s === null ? u = r : s.next = o, xe3(r, n.memoizedState) || (te = true), n.memoizedState = r, n.baseState = u, n.baseQueue = s, t.lastRenderedState = r;
    }
    if (e2 = t.interleaved, e2 !== null) {
      l = e2;
      do
        i = l.lane, R.lanes |= i, gn |= i, l = l.next;
      while (l !== e2);
    } else
      l === null && (t.lanes = 0);
    return [n.memoizedState, t.dispatch];
  }
  function yl(e2) {
    var n = ye3(), t = n.queue;
    if (t === null)
      throw Error(v(311));
    t.lastRenderedReducer = e2;
    var r = t.dispatch, l = t.pending, i = n.memoizedState;
    if (l !== null) {
      t.pending = null;
      var u = l = l.next;
      do
        i = e2(i, u.action), u = u.next;
      while (u !== l);
      xe3(i, n.memoizedState) || (te = true), n.memoizedState = i, n.baseQueue === null && (n.baseState = i), t.lastRenderedState = i;
    }
    return [i, r];
  }
  function ks() {
  }
  function Es(e2, n) {
    var t = R, r = ye3(), l = n(), i = !xe3(r.memoizedState, l);
    if (i && (r.memoizedState = l, te = true), r = r.queue, Qi(Ns.bind(null, t, r, e2), [e2]), r.getSnapshot !== n || i || W !== null && W.memoizedState.tag & 1) {
      if (t.flags |= 2048, Ot(9, xs.bind(null, t, r, l, n), void 0, null), Q === null)
        throw Error(v(349));
      (yn & 30) !== 0 || Cs(t, n, l);
    }
    return l;
  }
  function Cs(e2, n, t) {
    e2.flags |= 16384, e2 = { getSnapshot: n, value: t }, n = R.updateQueue, n === null ? (n = { lastEffect: null, stores: null }, R.updateQueue = n, n.stores = [e2]) : (t = n.stores, t === null ? n.stores = [e2] : t.push(e2));
  }
  function xs(e2, n, t, r) {
    n.value = t, n.getSnapshot = r, _s(n) && zs(e2);
  }
  function Ns(e2, n, t) {
    return t(function() {
      _s(n) && zs(e2);
    });
  }
  function _s(e2) {
    var n = e2.getSnapshot;
    e2 = e2.value;
    try {
      var t = n();
      return !xe3(e2, t);
    } catch {
      return true;
    }
  }
  function zs(e2) {
    var n = je2(e2, 1);
    n !== null && Ce2(n, e2, 1, -1);
  }
  function Yu(e2) {
    var n = _e3();
    return typeof e2 == "function" && (e2 = e2()), n.memoizedState = n.baseState = e2, e2 = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: Dt, lastRenderedState: e2 }, n.queue = e2, e2 = e2.dispatch = Zc.bind(null, R, e2), [n.memoizedState, e2];
  }
  function Ot(e2, n, t, r) {
    return e2 = { tag: e2, create: n, destroy: t, deps: r, next: null }, n = R.updateQueue, n === null ? (n = { lastEffect: null, stores: null }, R.updateQueue = n, n.lastEffect = e2.next = e2) : (t = n.lastEffect, t === null ? n.lastEffect = e2.next = e2 : (r = t.next, t.next = e2, e2.next = r, n.lastEffect = e2)), e2;
  }
  function Ps() {
    return ye3().memoizedState;
  }
  function ar(e2, n, t, r) {
    var l = _e3();
    R.flags |= e2, l.memoizedState = Ot(1 | n, t, void 0, r === void 0 ? null : r);
  }
  function $r(e2, n, t, r) {
    var l = ye3();
    r = r === void 0 ? null : r;
    var i = void 0;
    if (A2 !== null) {
      var u = A2.memoizedState;
      if (i = u.destroy, r !== null && Bi(r, u.deps)) {
        l.memoizedState = Ot(n, t, i, r);
        return;
      }
    }
    R.flags |= e2, l.memoizedState = Ot(1 | n, t, i, r);
  }
  function Xu(e2, n) {
    return ar(8390656, 8, e2, n);
  }
  function Qi(e2, n) {
    return $r(2048, 8, e2, n);
  }
  function Ls(e2, n) {
    return $r(4, 2, e2, n);
  }
  function Ts(e2, n) {
    return $r(4, 4, e2, n);
  }
  function Ms(e2, n) {
    if (typeof n == "function")
      return e2 = e2(), n(e2), function() {
        n(null);
      };
    if (n != null)
      return e2 = e2(), n.current = e2, function() {
        n.current = null;
      };
  }
  function Ds(e2, n, t) {
    return t = t != null ? t.concat([e2]) : null, $r(4, 4, Ms.bind(null, n, e2), t);
  }
  function $i() {
  }
  function Os(e2, n) {
    var t = ye3();
    n = n === void 0 ? null : n;
    var r = t.memoizedState;
    return r !== null && n !== null && Bi(n, r[1]) ? r[0] : (t.memoizedState = [e2, n], e2);
  }
  function Rs(e2, n) {
    var t = ye3();
    n = n === void 0 ? null : n;
    var r = t.memoizedState;
    return r !== null && n !== null && Bi(n, r[1]) ? r[0] : (e2 = e2(), t.memoizedState = [e2, n], e2);
  }
  function Fs(e2, n, t) {
    return (yn & 21) === 0 ? (e2.baseState && (e2.baseState = false, te = true), e2.memoizedState = t) : (xe3(t, n) || (t = Uo(), R.lanes |= t, gn |= t, e2.baseState = true), n);
  }
  function Xc(e2, n) {
    var t = P;
    P = t !== 0 && 4 > t ? t : 4, e2(true);
    var r = hl.transition;
    hl.transition = {};
    try {
      e2(false), n();
    } finally {
      P = t, hl.transition = r;
    }
  }
  function Is() {
    return ye3().memoizedState;
  }
  function Gc(e2, n, t) {
    var r = en(e2);
    if (t = { lane: r, action: t, hasEagerState: false, eagerState: null, next: null }, js(e2))
      Us(n, t);
    else if (t = ms(e2, n, t, r), t !== null) {
      var l = b();
      Ce2(t, e2, r, l), Vs(t, n, r);
    }
  }
  function Zc(e2, n, t) {
    var r = en(e2), l = { lane: r, action: t, hasEagerState: false, eagerState: null, next: null };
    if (js(e2))
      Us(n, l);
    else {
      var i = e2.alternate;
      if (e2.lanes === 0 && (i === null || i.lanes === 0) && (i = n.lastRenderedReducer, i !== null))
        try {
          var u = n.lastRenderedState, o = i(u, t);
          if (l.hasEagerState = true, l.eagerState = o, xe3(o, u)) {
            var s = n.interleaved;
            s === null ? (l.next = l, Ii(n)) : (l.next = s.next, s.next = l), n.interleaved = l;
            return;
          }
        } catch {
        } finally {
        }
      t = ms(e2, n, l, r), t !== null && (l = b(), Ce2(t, e2, r, l), Vs(t, n, r));
    }
  }
  function js(e2) {
    var n = e2.alternate;
    return e2 === R || n !== null && n === R;
  }
  function Us(e2, n) {
    mt = Mr = true;
    var t = e2.pending;
    t === null ? n.next = n : (n.next = t.next, t.next = n), e2.pending = n;
  }
  function Vs(e2, n, t) {
    if ((t & 4194240) !== 0) {
      var r = n.lanes;
      r &= e2.pendingLanes, t |= r, n.lanes = t, Ei(e2, t);
    }
  }
  var Dr = { readContext: ve3, useCallback: X2, useContext: X2, useEffect: X2, useImperativeHandle: X2, useInsertionEffect: X2, useLayoutEffect: X2, useMemo: X2, useReducer: X2, useRef: X2, useState: X2, useDebugValue: X2, useDeferredValue: X2, useTransition: X2, useMutableSource: X2, useSyncExternalStore: X2, useId: X2, unstable_isNewReconciler: false }, Jc = { readContext: ve3, useCallback: function(e2, n) {
    return _e3().memoizedState = [e2, n === void 0 ? null : n], e2;
  }, useContext: ve3, useEffect: Xu, useImperativeHandle: function(e2, n, t) {
    return t = t != null ? t.concat([e2]) : null, ar(4194308, 4, Ms.bind(null, n, e2), t);
  }, useLayoutEffect: function(e2, n) {
    return ar(4194308, 4, e2, n);
  }, useInsertionEffect: function(e2, n) {
    return ar(4, 2, e2, n);
  }, useMemo: function(e2, n) {
    var t = _e3();
    return n = n === void 0 ? null : n, e2 = e2(), t.memoizedState = [e2, n], e2;
  }, useReducer: function(e2, n, t) {
    var r = _e3();
    return n = t !== void 0 ? t(n) : n, r.memoizedState = r.baseState = n, e2 = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e2, lastRenderedState: n }, r.queue = e2, e2 = e2.dispatch = Gc.bind(null, R, e2), [r.memoizedState, e2];
  }, useRef: function(e2) {
    var n = _e3();
    return e2 = { current: e2 }, n.memoizedState = e2;
  }, useState: Yu, useDebugValue: $i, useDeferredValue: function(e2) {
    return _e3().memoizedState = e2;
  }, useTransition: function() {
    var e2 = Yu(false), n = e2[0];
    return e2 = Xc.bind(null, e2[1]), _e3().memoizedState = e2, [n, e2];
  }, useMutableSource: function() {
  }, useSyncExternalStore: function(e2, n, t) {
    var r = R, l = _e3();
    if (D2) {
      if (t === void 0)
        throw Error(v(407));
      t = t();
    } else {
      if (t = n(), Q === null)
        throw Error(v(349));
      (yn & 30) !== 0 || Cs(r, n, t);
    }
    l.memoizedState = t;
    var i = { value: t, getSnapshot: n };
    return l.queue = i, Xu(Ns.bind(null, r, i, e2), [e2]), r.flags |= 2048, Ot(9, xs.bind(null, r, i, t, n), void 0, null), t;
  }, useId: function() {
    var e2 = _e3(), n = Q.identifierPrefix;
    if (D2) {
      var t = Oe2, r = De2;
      t = (r & ~(1 << 32 - Ee2(r) - 1)).toString(32) + t, n = ":" + n + "R" + t, t = Mt++, 0 < t && (n += "H" + t.toString(32)), n += ":";
    } else
      t = Yc++, n = ":" + n + "r" + t.toString(32) + ":";
    return e2.memoizedState = n;
  }, unstable_isNewReconciler: false }, qc = { readContext: ve3, useCallback: Os, useContext: ve3, useEffect: Qi, useImperativeHandle: Ds, useInsertionEffect: Ls, useLayoutEffect: Ts, useMemo: Rs, useReducer: vl, useRef: Ps, useState: function() {
    return vl(Dt);
  }, useDebugValue: $i, useDeferredValue: function(e2) {
    var n = ye3();
    return Fs(n, A2.memoizedState, e2);
  }, useTransition: function() {
    var e2 = vl(Dt)[0], n = ye3().memoizedState;
    return [e2, n];
  }, useMutableSource: ks, useSyncExternalStore: Es, useId: Is, unstable_isNewReconciler: false }, bc = { readContext: ve3, useCallback: Os, useContext: ve3, useEffect: Qi, useImperativeHandle: Ds, useInsertionEffect: Ls, useLayoutEffect: Ts, useMemo: Rs, useReducer: yl, useRef: Ps, useState: function() {
    return yl(Dt);
  }, useDebugValue: $i, useDeferredValue: function(e2) {
    var n = ye3();
    return A2 === null ? n.memoizedState = e2 : Fs(n, A2.memoizedState, e2);
  }, useTransition: function() {
    var e2 = yl(Dt)[0], n = ye3().memoizedState;
    return [e2, n];
  }, useMutableSource: ks, useSyncExternalStore: Es, useId: Is, unstable_isNewReconciler: false };
  function Yn(e2, n) {
    try {
      var t = "", r = n;
      do
        t += La(r), r = r.return;
      while (r);
      var l = t;
    } catch (i) {
      l = `
Error generating stack: ` + i.message + `
` + i.stack;
    }
    return { value: e2, source: n, stack: l, digest: null };
  }
  function gl(e2, n, t) {
    return { value: e2, source: null, stack: t ?? null, digest: n ?? null };
  }
  function ei(e2, n) {
    try {
      console.error(n.value);
    } catch (t) {
      setTimeout(function() {
        throw t;
      });
    }
  }
  var ef = typeof WeakMap == "function" ? WeakMap : Map;
  function As(e2, n, t) {
    t = Re2(-1, t), t.tag = 3, t.payload = { element: null };
    var r = n.value;
    return t.callback = function() {
      Rr || (Rr = true, ci = r), ei(e2, n);
    }, t;
  }
  function Bs(e2, n, t) {
    t = Re2(-1, t), t.tag = 3;
    var r = e2.type.getDerivedStateFromError;
    if (typeof r == "function") {
      var l = n.value;
      t.payload = function() {
        return r(l);
      }, t.callback = function() {
        ei(e2, n);
      };
    }
    var i = e2.stateNode;
    return i !== null && typeof i.componentDidCatch == "function" && (t.callback = function() {
      ei(e2, n), typeof r != "function" && (be3 === null ? be3 = new Set([this]) : be3.add(this));
      var u = n.stack;
      this.componentDidCatch(n.value, { componentStack: u !== null ? u : "" });
    }), t;
  }
  function Gu(e2, n, t) {
    var r = e2.pingCache;
    if (r === null) {
      r = e2.pingCache = new ef();
      var l = new Set();
      r.set(n, l);
    } else
      l = r.get(n), l === void 0 && (l = new Set(), r.set(n, l));
    l.has(t) || (l.add(t), e2 = hf.bind(null, e2, n, t), n.then(e2, e2));
  }
  function Zu(e2) {
    do {
      var n;
      if ((n = e2.tag === 13) && (n = e2.memoizedState, n = n !== null ? n.dehydrated !== null : true), n)
        return e2;
      e2 = e2.return;
    } while (e2 !== null);
    return null;
  }
  function Ju(e2, n, t, r, l) {
    return (e2.mode & 1) === 0 ? (e2 === n ? e2.flags |= 65536 : (e2.flags |= 128, t.flags |= 131072, t.flags &= -52805, t.tag === 1 && (t.alternate === null ? t.tag = 17 : (n = Re2(-1, 1), n.tag = 2, qe2(t, n, 1))), t.lanes |= 1), e2) : (e2.flags |= 65536, e2.lanes = l, e2);
  }
  var nf = Ve2.ReactCurrentOwner, te = false;
  function q2(e2, n, t, r) {
    n.child = e2 === null ? ws(n, null, t, r) : $n(n, e2.child, t, r);
  }
  function qu(e2, n, t, r, l) {
    t = t.render;
    var i = n.ref;
    return An(n, l), r = Hi(e2, n, t, r, i, l), t = Wi(), e2 !== null && !te ? (n.updateQueue = e2.updateQueue, n.flags &= -2053, e2.lanes &= ~l, Ue2(e2, n, l)) : (D2 && t && Ti(n), n.flags |= 1, q2(e2, n, r, l), n.child);
  }
  function bu(e2, n, t, r, l) {
    if (e2 === null) {
      var i = t.type;
      return typeof i == "function" && !bi(i) && i.defaultProps === void 0 && t.compare === null && t.defaultProps === void 0 ? (n.tag = 15, n.type = i, Hs(e2, n, i, r, l)) : (e2 = pr(t.type, null, r, n, n.mode, l), e2.ref = n.ref, e2.return = n, n.child = e2);
    }
    if (i = e2.child, (e2.lanes & l) === 0) {
      var u = i.memoizedProps;
      if (t = t.compare, t = t !== null ? t : Nt, t(u, r) && e2.ref === n.ref)
        return Ue2(e2, n, l);
    }
    return n.flags |= 1, e2 = nn(i, r), e2.ref = n.ref, e2.return = n, n.child = e2;
  }
  function Hs(e2, n, t, r, l) {
    if (e2 !== null) {
      var i = e2.memoizedProps;
      if (Nt(i, r) && e2.ref === n.ref)
        if (te = false, n.pendingProps = r = i, (e2.lanes & l) !== 0)
          (e2.flags & 131072) !== 0 && (te = true);
        else
          return n.lanes = e2.lanes, Ue2(e2, n, l);
    }
    return ni(e2, n, t, r, l);
  }
  function Ws(e2, n, t) {
    var r = n.pendingProps, l = r.children, i = e2 !== null ? e2.memoizedState : null;
    if (r.mode === "hidden")
      if ((n.mode & 1) === 0)
        n.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, L(Fn, ue2), ue2 |= t;
      else {
        if ((t & 1073741824) === 0)
          return e2 = i !== null ? i.baseLanes | t : t, n.lanes = n.childLanes = 1073741824, n.memoizedState = { baseLanes: e2, cachePool: null, transitions: null }, n.updateQueue = null, L(Fn, ue2), ue2 |= e2, null;
        n.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : t, L(Fn, ue2), ue2 |= r;
      }
    else
      i !== null ? (r = i.baseLanes | t, n.memoizedState = null) : r = t, L(Fn, ue2), ue2 |= r;
    return q2(e2, n, l, t), n.child;
  }
  function Qs(e2, n) {
    var t = n.ref;
    (e2 === null && t !== null || e2 !== null && e2.ref !== t) && (n.flags |= 512, n.flags |= 2097152);
  }
  function ni(e2, n, t, r, l) {
    var i = le2(t) ? hn : J.current;
    return i = Wn(n, i), An(n, l), t = Hi(e2, n, t, r, i, l), r = Wi(), e2 !== null && !te ? (n.updateQueue = e2.updateQueue, n.flags &= -2053, e2.lanes &= ~l, Ue2(e2, n, l)) : (D2 && r && Ti(n), n.flags |= 1, q2(e2, n, t, l), n.child);
  }
  function eo(e2, n, t, r, l) {
    if (le2(t)) {
      var i = true;
      xr(n);
    } else
      i = false;
    if (An(n, l), n.stateNode === null)
      cr(e2, n), ys(n, t, r), bl(n, t, r, l), r = true;
    else if (e2 === null) {
      var u = n.stateNode, o = n.memoizedProps;
      u.props = o;
      var s = u.context, d = t.contextType;
      typeof d == "object" && d !== null ? d = ve3(d) : (d = le2(t) ? hn : J.current, d = Wn(n, d));
      var m = t.getDerivedStateFromProps, h2 = typeof m == "function" || typeof u.getSnapshotBeforeUpdate == "function";
      h2 || typeof u.UNSAFE_componentWillReceiveProps != "function" && typeof u.componentWillReceiveProps != "function" || (o !== r || s !== d) && $u(n, u, r, d), We = false;
      var p = n.memoizedState;
      u.state = p, Lr(n, r, u, l), s = n.memoizedState, o !== r || p !== s || re.current || We ? (typeof m == "function" && (ql(n, t, m, r), s = n.memoizedState), (o = We || Qu(n, t, o, r, p, s, d)) ? (h2 || typeof u.UNSAFE_componentWillMount != "function" && typeof u.componentWillMount != "function" || (typeof u.componentWillMount == "function" && u.componentWillMount(), typeof u.UNSAFE_componentWillMount == "function" && u.UNSAFE_componentWillMount()), typeof u.componentDidMount == "function" && (n.flags |= 4194308)) : (typeof u.componentDidMount == "function" && (n.flags |= 4194308), n.memoizedProps = r, n.memoizedState = s), u.props = r, u.state = s, u.context = d, r = o) : (typeof u.componentDidMount == "function" && (n.flags |= 4194308), r = false);
    } else {
      u = n.stateNode, hs(e2, n), o = n.memoizedProps, d = n.type === n.elementType ? o : we3(n.type, o), u.props = d, h2 = n.pendingProps, p = u.context, s = t.contextType, typeof s == "object" && s !== null ? s = ve3(s) : (s = le2(t) ? hn : J.current, s = Wn(n, s));
      var g = t.getDerivedStateFromProps;
      (m = typeof g == "function" || typeof u.getSnapshotBeforeUpdate == "function") || typeof u.UNSAFE_componentWillReceiveProps != "function" && typeof u.componentWillReceiveProps != "function" || (o !== h2 || p !== s) && $u(n, u, r, s), We = false, p = n.memoizedState, u.state = p, Lr(n, r, u, l);
      var S2 = n.memoizedState;
      o !== h2 || p !== S2 || re.current || We ? (typeof g == "function" && (ql(n, t, g, r), S2 = n.memoizedState), (d = We || Qu(n, t, d, r, p, S2, s) || false) ? (m || typeof u.UNSAFE_componentWillUpdate != "function" && typeof u.componentWillUpdate != "function" || (typeof u.componentWillUpdate == "function" && u.componentWillUpdate(r, S2, s), typeof u.UNSAFE_componentWillUpdate == "function" && u.UNSAFE_componentWillUpdate(r, S2, s)), typeof u.componentDidUpdate == "function" && (n.flags |= 4), typeof u.getSnapshotBeforeUpdate == "function" && (n.flags |= 1024)) : (typeof u.componentDidUpdate != "function" || o === e2.memoizedProps && p === e2.memoizedState || (n.flags |= 4), typeof u.getSnapshotBeforeUpdate != "function" || o === e2.memoizedProps && p === e2.memoizedState || (n.flags |= 1024), n.memoizedProps = r, n.memoizedState = S2), u.props = r, u.state = S2, u.context = s, r = d) : (typeof u.componentDidUpdate != "function" || o === e2.memoizedProps && p === e2.memoizedState || (n.flags |= 4), typeof u.getSnapshotBeforeUpdate != "function" || o === e2.memoizedProps && p === e2.memoizedState || (n.flags |= 1024), r = false);
    }
    return ti(e2, n, t, r, i, l);
  }
  function ti(e2, n, t, r, l, i) {
    Qs(e2, n);
    var u = (n.flags & 128) !== 0;
    if (!r && !u)
      return l && Vu(n, t, false), Ue2(e2, n, i);
    r = n.stateNode, nf.current = n;
    var o = u && typeof t.getDerivedStateFromError != "function" ? null : r.render();
    return n.flags |= 1, e2 !== null && u ? (n.child = $n(n, e2.child, null, i), n.child = $n(n, null, o, i)) : q2(e2, n, o, i), n.memoizedState = r.state, l && Vu(n, t, true), n.child;
  }
  function $s(e2) {
    var n = e2.stateNode;
    n.pendingContext ? Uu(e2, n.pendingContext, n.pendingContext !== n.context) : n.context && Uu(e2, n.context, false), Ui(e2, n.containerInfo);
  }
  function no(e2, n, t, r, l) {
    return Qn(), Di(l), n.flags |= 256, q2(e2, n, t, r), n.child;
  }
  var ri = { dehydrated: null, treeContext: null, retryLane: 0 };
  function li(e2) {
    return { baseLanes: e2, cachePool: null, transitions: null };
  }
  function Ks(e2, n, t) {
    var r = n.pendingProps, l = O.current, i = false, u = (n.flags & 128) !== 0, o;
    if ((o = u) || (o = e2 !== null && e2.memoizedState === null ? false : (l & 2) !== 0), o ? (i = true, n.flags &= -129) : (e2 === null || e2.memoizedState !== null) && (l |= 1), L(O, l & 1), e2 === null)
      return Zl(n), e2 = n.memoizedState, e2 !== null && (e2 = e2.dehydrated, e2 !== null) ? ((n.mode & 1) === 0 ? n.lanes = 1 : e2.data === "$!" ? n.lanes = 8 : n.lanes = 1073741824, null) : (u = r.children, e2 = r.fallback, i ? (r = n.mode, i = n.child, u = { mode: "hidden", children: u }, (r & 1) === 0 && i !== null ? (i.childLanes = 0, i.pendingProps = u) : i = Xr(u, r, 0, null), e2 = mn(e2, r, t, null), i.return = n, e2.return = n, i.sibling = e2, n.child = i, n.child.memoizedState = li(t), n.memoizedState = ri, e2) : Ki(n, u));
    if (l = e2.memoizedState, l !== null && (o = l.dehydrated, o !== null))
      return tf(e2, n, u, r, o, l, t);
    if (i) {
      i = r.fallback, u = n.mode, l = e2.child, o = l.sibling;
      var s = { mode: "hidden", children: r.children };
      return (u & 1) === 0 && n.child !== l ? (r = n.child, r.childLanes = 0, r.pendingProps = s, n.deletions = null) : (r = nn(l, s), r.subtreeFlags = l.subtreeFlags & 14680064), o !== null ? i = nn(o, i) : (i = mn(i, u, t, null), i.flags |= 2), i.return = n, r.return = n, r.sibling = i, n.child = r, r = i, i = n.child, u = e2.child.memoizedState, u = u === null ? li(t) : { baseLanes: u.baseLanes | t, cachePool: null, transitions: u.transitions }, i.memoizedState = u, i.childLanes = e2.childLanes & ~t, n.memoizedState = ri, r;
    }
    return i = e2.child, e2 = i.sibling, r = nn(i, { mode: "visible", children: r.children }), (n.mode & 1) === 0 && (r.lanes = t), r.return = n, r.sibling = null, e2 !== null && (t = n.deletions, t === null ? (n.deletions = [e2], n.flags |= 16) : t.push(e2)), n.child = r, n.memoizedState = null, r;
  }
  function Ki(e2, n) {
    return n = Xr({ mode: "visible", children: n }, e2.mode, 0, null), n.return = e2, e2.child = n;
  }
  function nr(e2, n, t, r) {
    return r !== null && Di(r), $n(n, e2.child, null, t), e2 = Ki(n, n.pendingProps.children), e2.flags |= 2, n.memoizedState = null, e2;
  }
  function tf(e2, n, t, r, l, i, u) {
    if (t)
      return n.flags & 256 ? (n.flags &= -257, r = gl(Error(v(422))), nr(e2, n, u, r)) : n.memoizedState !== null ? (n.child = e2.child, n.flags |= 128, null) : (i = r.fallback, l = n.mode, r = Xr({ mode: "visible", children: r.children }, l, 0, null), i = mn(i, l, u, null), i.flags |= 2, r.return = n, i.return = n, r.sibling = i, n.child = r, (n.mode & 1) !== 0 && $n(n, e2.child, null, u), n.child.memoizedState = li(u), n.memoizedState = ri, i);
    if ((n.mode & 1) === 0)
      return nr(e2, n, u, null);
    if (l.data === "$!") {
      if (r = l.nextSibling && l.nextSibling.dataset, r)
        var o = r.dgst;
      return r = o, i = Error(v(419)), r = gl(i, r, void 0), nr(e2, n, u, r);
    }
    if (o = (u & e2.childLanes) !== 0, te || o) {
      if (r = Q, r !== null) {
        switch (u & -u) {
          case 4:
            l = 2;
            break;
          case 16:
            l = 8;
            break;
          case 64:
          case 128:
          case 256:
          case 512:
          case 1024:
          case 2048:
          case 4096:
          case 8192:
          case 16384:
          case 32768:
          case 65536:
          case 131072:
          case 262144:
          case 524288:
          case 1048576:
          case 2097152:
          case 4194304:
          case 8388608:
          case 16777216:
          case 33554432:
          case 67108864:
            l = 32;
            break;
          case 536870912:
            l = 268435456;
            break;
          default:
            l = 0;
        }
        l = (l & (r.suspendedLanes | u)) !== 0 ? 0 : l, l !== 0 && l !== i.retryLane && (i.retryLane = l, je2(e2, l), Ce2(r, e2, l, -1));
      }
      return qi(), r = gl(Error(v(421))), nr(e2, n, u, r);
    }
    return l.data === "$?" ? (n.flags |= 128, n.child = e2.child, n = vf.bind(null, e2), l._reactRetry = n, null) : (e2 = i.treeContext, oe2 = Je(l.nextSibling), se2 = n, D2 = true, ke3 = null, e2 !== null && (de3[pe3++] = De2, de3[pe3++] = Oe2, de3[pe3++] = vn, De2 = e2.id, Oe2 = e2.overflow, vn = n), n = Ki(n, r.children), n.flags |= 4096, n);
  }
  function to(e2, n, t) {
    e2.lanes |= n;
    var r = e2.alternate;
    r !== null && (r.lanes |= n), Jl(e2.return, n, t);
  }
  function wl(e2, n, t, r, l) {
    var i = e2.memoizedState;
    i === null ? e2.memoizedState = { isBackwards: n, rendering: null, renderingStartTime: 0, last: r, tail: t, tailMode: l } : (i.isBackwards = n, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = t, i.tailMode = l);
  }
  function Ys(e2, n, t) {
    var r = n.pendingProps, l = r.revealOrder, i = r.tail;
    if (q2(e2, n, r.children, t), r = O.current, (r & 2) !== 0)
      r = r & 1 | 2, n.flags |= 128;
    else {
      if (e2 !== null && (e2.flags & 128) !== 0)
        e:
          for (e2 = n.child; e2 !== null; ) {
            if (e2.tag === 13)
              e2.memoizedState !== null && to(e2, t, n);
            else if (e2.tag === 19)
              to(e2, t, n);
            else if (e2.child !== null) {
              e2.child.return = e2, e2 = e2.child;
              continue;
            }
            if (e2 === n)
              break e;
            for (; e2.sibling === null; ) {
              if (e2.return === null || e2.return === n)
                break e;
              e2 = e2.return;
            }
            e2.sibling.return = e2.return, e2 = e2.sibling;
          }
      r &= 1;
    }
    if (L(O, r), (n.mode & 1) === 0)
      n.memoizedState = null;
    else
      switch (l) {
        case "forwards":
          for (t = n.child, l = null; t !== null; )
            e2 = t.alternate, e2 !== null && Tr(e2) === null && (l = t), t = t.sibling;
          t = l, t === null ? (l = n.child, n.child = null) : (l = t.sibling, t.sibling = null), wl(n, false, l, t, i);
          break;
        case "backwards":
          for (t = null, l = n.child, n.child = null; l !== null; ) {
            if (e2 = l.alternate, e2 !== null && Tr(e2) === null) {
              n.child = l;
              break;
            }
            e2 = l.sibling, l.sibling = t, t = l, l = e2;
          }
          wl(n, true, t, null, i);
          break;
        case "together":
          wl(n, false, null, null, void 0);
          break;
        default:
          n.memoizedState = null;
      }
    return n.child;
  }
  function cr(e2, n) {
    (n.mode & 1) === 0 && e2 !== null && (e2.alternate = null, n.alternate = null, n.flags |= 2);
  }
  function Ue2(e2, n, t) {
    if (e2 !== null && (n.dependencies = e2.dependencies), gn |= n.lanes, (t & n.childLanes) === 0)
      return null;
    if (e2 !== null && n.child !== e2.child)
      throw Error(v(153));
    if (n.child !== null) {
      for (e2 = n.child, t = nn(e2, e2.pendingProps), n.child = t, t.return = n; e2.sibling !== null; )
        e2 = e2.sibling, t = t.sibling = nn(e2, e2.pendingProps), t.return = n;
      t.sibling = null;
    }
    return n.child;
  }
  function rf(e2, n, t) {
    switch (n.tag) {
      case 3:
        $s(n), Qn();
        break;
      case 5:
        Ss(n);
        break;
      case 1:
        le2(n.type) && xr(n);
        break;
      case 4:
        Ui(n, n.stateNode.containerInfo);
        break;
      case 10:
        var r = n.type._context, l = n.memoizedProps.value;
        L(zr, r._currentValue), r._currentValue = l;
        break;
      case 13:
        if (r = n.memoizedState, r !== null)
          return r.dehydrated !== null ? (L(O, O.current & 1), n.flags |= 128, null) : (t & n.child.childLanes) !== 0 ? Ks(e2, n, t) : (L(O, O.current & 1), e2 = Ue2(e2, n, t), e2 !== null ? e2.sibling : null);
        L(O, O.current & 1);
        break;
      case 19:
        if (r = (t & n.childLanes) !== 0, (e2.flags & 128) !== 0) {
          if (r)
            return Ys(e2, n, t);
          n.flags |= 128;
        }
        if (l = n.memoizedState, l !== null && (l.rendering = null, l.tail = null, l.lastEffect = null), L(O, O.current), r)
          break;
        return null;
      case 22:
      case 23:
        return n.lanes = 0, Ws(e2, n, t);
    }
    return Ue2(e2, n, t);
  }
  var Xs, ii, Gs, Zs;
  Xs = function(e2, n) {
    for (var t = n.child; t !== null; ) {
      if (t.tag === 5 || t.tag === 6)
        e2.appendChild(t.stateNode);
      else if (t.tag !== 4 && t.child !== null) {
        t.child.return = t, t = t.child;
        continue;
      }
      if (t === n)
        break;
      for (; t.sibling === null; ) {
        if (t.return === null || t.return === n)
          return;
        t = t.return;
      }
      t.sibling.return = t.return, t = t.sibling;
    }
  };
  ii = function() {
  };
  Gs = function(e2, n, t, r) {
    var l = e2.memoizedProps;
    if (l !== r) {
      e2 = n.stateNode, dn(Le2.current);
      var i = null;
      switch (t) {
        case "input":
          l = zl(e2, l), r = zl(e2, r), i = [];
          break;
        case "select":
          l = F2({}, l, { value: void 0 }), r = F2({}, r, { value: void 0 }), i = [];
          break;
        case "textarea":
          l = Tl(e2, l), r = Tl(e2, r), i = [];
          break;
        default:
          typeof l.onClick != "function" && typeof r.onClick == "function" && (e2.onclick = Er);
      }
      Dl(t, r);
      var u;
      t = null;
      for (d in l)
        if (!r.hasOwnProperty(d) && l.hasOwnProperty(d) && l[d] != null)
          if (d === "style") {
            var o = l[d];
            for (u in o)
              o.hasOwnProperty(u) && (t || (t = {}), t[u] = "");
          } else
            d !== "dangerouslySetInnerHTML" && d !== "children" && d !== "suppressContentEditableWarning" && d !== "suppressHydrationWarning" && d !== "autoFocus" && (gt.hasOwnProperty(d) ? i || (i = []) : (i = i || []).push(d, null));
      for (d in r) {
        var s = r[d];
        if (o = l?.[d], r.hasOwnProperty(d) && s !== o && (s != null || o != null))
          if (d === "style")
            if (o) {
              for (u in o)
                !o.hasOwnProperty(u) || s && s.hasOwnProperty(u) || (t || (t = {}), t[u] = "");
              for (u in s)
                s.hasOwnProperty(u) && o[u] !== s[u] && (t || (t = {}), t[u] = s[u]);
            } else
              t || (i || (i = []), i.push(d, t)), t = s;
          else
            d === "dangerouslySetInnerHTML" ? (s = s ? s.__html : void 0, o = o ? o.__html : void 0, s != null && o !== s && (i = i || []).push(d, s)) : d === "children" ? typeof s != "string" && typeof s != "number" || (i = i || []).push(d, "" + s) : d !== "suppressContentEditableWarning" && d !== "suppressHydrationWarning" && (gt.hasOwnProperty(d) ? (s != null && d === "onScroll" && T("scroll", e2), i || o === s || (i = [])) : (i = i || []).push(d, s));
      }
      t && (i = i || []).push("style", t);
      var d = i;
      (n.updateQueue = d) && (n.flags |= 4);
    }
  };
  Zs = function(e2, n, t, r) {
    t !== r && (n.flags |= 4);
  };
  function tt(e2, n) {
    if (!D2)
      switch (e2.tailMode) {
        case "hidden":
          n = e2.tail;
          for (var t = null; n !== null; )
            n.alternate !== null && (t = n), n = n.sibling;
          t === null ? e2.tail = null : t.sibling = null;
          break;
        case "collapsed":
          t = e2.tail;
          for (var r = null; t !== null; )
            t.alternate !== null && (r = t), t = t.sibling;
          r === null ? n || e2.tail === null ? e2.tail = null : e2.tail.sibling = null : r.sibling = null;
      }
  }
  function G(e2) {
    var n = e2.alternate !== null && e2.alternate.child === e2.child, t = 0, r = 0;
    if (n)
      for (var l = e2.child; l !== null; )
        t |= l.lanes | l.childLanes, r |= l.subtreeFlags & 14680064, r |= l.flags & 14680064, l.return = e2, l = l.sibling;
    else
      for (l = e2.child; l !== null; )
        t |= l.lanes | l.childLanes, r |= l.subtreeFlags, r |= l.flags, l.return = e2, l = l.sibling;
    return e2.subtreeFlags |= r, e2.childLanes = t, n;
  }
  function lf(e2, n, t) {
    var r = n.pendingProps;
    switch (Mi(n), n.tag) {
      case 2:
      case 16:
      case 15:
      case 0:
      case 11:
      case 7:
      case 8:
      case 12:
      case 9:
      case 14:
        return G(n), null;
      case 1:
        return le2(n.type) && Cr(), G(n), null;
      case 3:
        return r = n.stateNode, Kn(), M2(re), M2(J), Ai(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e2 === null || e2.child === null) && (bt(n) ? n.flags |= 4 : e2 === null || e2.memoizedState.isDehydrated && (n.flags & 256) === 0 || (n.flags |= 1024, ke3 !== null && (pi(ke3), ke3 = null))), ii(e2, n), G(n), null;
      case 5:
        Vi(n);
        var l = dn(Tt.current);
        if (t = n.type, e2 !== null && n.stateNode != null)
          Gs(e2, n, t, r, l), e2.ref !== n.ref && (n.flags |= 512, n.flags |= 2097152);
        else {
          if (!r) {
            if (n.stateNode === null)
              throw Error(v(166));
            return G(n), null;
          }
          if (e2 = dn(Le2.current), bt(n)) {
            r = n.stateNode, t = n.type;
            var i = n.memoizedProps;
            switch (r[ze2] = n, r[Pt] = i, e2 = (n.mode & 1) !== 0, t) {
              case "dialog":
                T("cancel", r), T("close", r);
                break;
              case "iframe":
              case "object":
              case "embed":
                T("load", r);
                break;
              case "video":
              case "audio":
                for (l = 0; l < st.length; l++)
                  T(st[l], r);
                break;
              case "source":
                T("error", r);
                break;
              case "img":
              case "image":
              case "link":
                T("error", r), T("load", r);
                break;
              case "details":
                T("toggle", r);
                break;
              case "input":
                cu(r, i), T("invalid", r);
                break;
              case "select":
                r._wrapperState = { wasMultiple: !!i.multiple }, T("invalid", r);
                break;
              case "textarea":
                du(r, i), T("invalid", r);
            }
            Dl(t, i), l = null;
            for (var u in i)
              if (i.hasOwnProperty(u)) {
                var o = i[u];
                u === "children" ? typeof o == "string" ? r.textContent !== o && (i.suppressHydrationWarning !== true && qt(r.textContent, o, e2), l = ["children", o]) : typeof o == "number" && r.textContent !== "" + o && (i.suppressHydrationWarning !== true && qt(r.textContent, o, e2), l = ["children", "" + o]) : gt.hasOwnProperty(u) && o != null && u === "onScroll" && T("scroll", r);
              }
            switch (t) {
              case "input":
                At(r), fu(r, i, true);
                break;
              case "textarea":
                At(r), pu(r);
                break;
              case "select":
              case "option":
                break;
              default:
                typeof i.onClick == "function" && (r.onclick = Er);
            }
            r = l, n.updateQueue = r, r !== null && (n.flags |= 4);
          } else {
            u = l.nodeType === 9 ? l : l.ownerDocument, e2 === "http://www.w3.org/1999/xhtml" && (e2 = Co(t)), e2 === "http://www.w3.org/1999/xhtml" ? t === "script" ? (e2 = u.createElement("div"), e2.innerHTML = "<script><\/script>", e2 = e2.removeChild(e2.firstChild)) : typeof r.is == "string" ? e2 = u.createElement(t, { is: r.is }) : (e2 = u.createElement(t), t === "select" && (u = e2, r.multiple ? u.multiple = true : r.size && (u.size = r.size))) : e2 = u.createElementNS(e2, t), e2[ze2] = n, e2[Pt] = r, Xs(e2, n, false, false), n.stateNode = e2;
            e: {
              switch (u = Ol(t, r), t) {
                case "dialog":
                  T("cancel", e2), T("close", e2), l = r;
                  break;
                case "iframe":
                case "object":
                case "embed":
                  T("load", e2), l = r;
                  break;
                case "video":
                case "audio":
                  for (l = 0; l < st.length; l++)
                    T(st[l], e2);
                  l = r;
                  break;
                case "source":
                  T("error", e2), l = r;
                  break;
                case "img":
                case "image":
                case "link":
                  T("error", e2), T("load", e2), l = r;
                  break;
                case "details":
                  T("toggle", e2), l = r;
                  break;
                case "input":
                  cu(e2, r), l = zl(e2, r), T("invalid", e2);
                  break;
                case "option":
                  l = r;
                  break;
                case "select":
                  e2._wrapperState = { wasMultiple: !!r.multiple }, l = F2({}, r, { value: void 0 }), T("invalid", e2);
                  break;
                case "textarea":
                  du(e2, r), l = Tl(e2, r), T("invalid", e2);
                  break;
                default:
                  l = r;
              }
              Dl(t, l), o = l;
              for (i in o)
                if (o.hasOwnProperty(i)) {
                  var s = o[i];
                  i === "style" ? _o(e2, s) : i === "dangerouslySetInnerHTML" ? (s = s ? s.__html : void 0, s != null && xo(e2, s)) : i === "children" ? typeof s == "string" ? (t !== "textarea" || s !== "") && wt(e2, s) : typeof s == "number" && wt(e2, "" + s) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (gt.hasOwnProperty(i) ? s != null && i === "onScroll" && T("scroll", e2) : s != null && vi(e2, i, s, u));
                }
              switch (t) {
                case "input":
                  At(e2), fu(e2, r, false);
                  break;
                case "textarea":
                  At(e2), pu(e2);
                  break;
                case "option":
                  r.value != null && e2.setAttribute("value", "" + tn(r.value));
                  break;
                case "select":
                  e2.multiple = !!r.multiple, i = r.value, i != null ? In(e2, !!r.multiple, i, false) : r.defaultValue != null && In(e2, !!r.multiple, r.defaultValue, true);
                  break;
                default:
                  typeof l.onClick == "function" && (e2.onclick = Er);
              }
              switch (t) {
                case "button":
                case "input":
                case "select":
                case "textarea":
                  r = !!r.autoFocus;
                  break e;
                case "img":
                  r = true;
                  break e;
                default:
                  r = false;
              }
            }
            r && (n.flags |= 4);
          }
          n.ref !== null && (n.flags |= 512, n.flags |= 2097152);
        }
        return G(n), null;
      case 6:
        if (e2 && n.stateNode != null)
          Zs(e2, n, e2.memoizedProps, r);
        else {
          if (typeof r != "string" && n.stateNode === null)
            throw Error(v(166));
          if (t = dn(Tt.current), dn(Le2.current), bt(n)) {
            if (r = n.stateNode, t = n.memoizedProps, r[ze2] = n, (i = r.nodeValue !== t) && (e2 = se2, e2 !== null))
              switch (e2.tag) {
                case 3:
                  qt(r.nodeValue, t, (e2.mode & 1) !== 0);
                  break;
                case 5:
                  e2.memoizedProps.suppressHydrationWarning !== true && qt(r.nodeValue, t, (e2.mode & 1) !== 0);
              }
            i && (n.flags |= 4);
          } else
            r = (t.nodeType === 9 ? t : t.ownerDocument).createTextNode(r), r[ze2] = n, n.stateNode = r;
        }
        return G(n), null;
      case 13:
        if (M2(O), r = n.memoizedState, e2 === null || e2.memoizedState !== null && e2.memoizedState.dehydrated !== null) {
          if (D2 && oe2 !== null && (n.mode & 1) !== 0 && (n.flags & 128) === 0)
            ps(), Qn(), n.flags |= 98560, i = false;
          else if (i = bt(n), r !== null && r.dehydrated !== null) {
            if (e2 === null) {
              if (!i)
                throw Error(v(318));
              if (i = n.memoizedState, i = i !== null ? i.dehydrated : null, !i)
                throw Error(v(317));
              i[ze2] = n;
            } else
              Qn(), (n.flags & 128) === 0 && (n.memoizedState = null), n.flags |= 4;
            G(n), i = false;
          } else
            ke3 !== null && (pi(ke3), ke3 = null), i = true;
          if (!i)
            return n.flags & 65536 ? n : null;
        }
        return (n.flags & 128) !== 0 ? (n.lanes = t, n) : (r = r !== null, r !== (e2 !== null && e2.memoizedState !== null) && r && (n.child.flags |= 8192, (n.mode & 1) !== 0 && (e2 === null || (O.current & 1) !== 0 ? B3 === 0 && (B3 = 3) : qi())), n.updateQueue !== null && (n.flags |= 4), G(n), null);
      case 4:
        return Kn(), ii(e2, n), e2 === null && _t(n.stateNode.containerInfo), G(n), null;
      case 10:
        return Fi(n.type._context), G(n), null;
      case 17:
        return le2(n.type) && Cr(), G(n), null;
      case 19:
        if (M2(O), i = n.memoizedState, i === null)
          return G(n), null;
        if (r = (n.flags & 128) !== 0, u = i.rendering, u === null)
          if (r)
            tt(i, false);
          else {
            if (B3 !== 0 || e2 !== null && (e2.flags & 128) !== 0)
              for (e2 = n.child; e2 !== null; ) {
                if (u = Tr(e2), u !== null) {
                  for (n.flags |= 128, tt(i, false), r = u.updateQueue, r !== null && (n.updateQueue = r, n.flags |= 4), n.subtreeFlags = 0, r = t, t = n.child; t !== null; )
                    i = t, e2 = r, i.flags &= 14680066, u = i.alternate, u === null ? (i.childLanes = 0, i.lanes = e2, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = u.childLanes, i.lanes = u.lanes, i.child = u.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = u.memoizedProps, i.memoizedState = u.memoizedState, i.updateQueue = u.updateQueue, i.type = u.type, e2 = u.dependencies, i.dependencies = e2 === null ? null : { lanes: e2.lanes, firstContext: e2.firstContext }), t = t.sibling;
                  return L(O, O.current & 1 | 2), n.child;
                }
                e2 = e2.sibling;
              }
            i.tail !== null && U3() > Xn && (n.flags |= 128, r = true, tt(i, false), n.lanes = 4194304);
          }
        else {
          if (!r)
            if (e2 = Tr(u), e2 !== null) {
              if (n.flags |= 128, r = true, t = e2.updateQueue, t !== null && (n.updateQueue = t, n.flags |= 4), tt(i, true), i.tail === null && i.tailMode === "hidden" && !u.alternate && !D2)
                return G(n), null;
            } else
              2 * U3() - i.renderingStartTime > Xn && t !== 1073741824 && (n.flags |= 128, r = true, tt(i, false), n.lanes = 4194304);
          i.isBackwards ? (u.sibling = n.child, n.child = u) : (t = i.last, t !== null ? t.sibling = u : n.child = u, i.last = u);
        }
        return i.tail !== null ? (n = i.tail, i.rendering = n, i.tail = n.sibling, i.renderingStartTime = U3(), n.sibling = null, t = O.current, L(O, r ? t & 1 | 2 : t & 1), n) : (G(n), null);
      case 22:
      case 23:
        return Ji(), r = n.memoizedState !== null, e2 !== null && e2.memoizedState !== null !== r && (n.flags |= 8192), r && (n.mode & 1) !== 0 ? (ue2 & 1073741824) !== 0 && (G(n), n.subtreeFlags & 6 && (n.flags |= 8192)) : G(n), null;
      case 24:
        return null;
      case 25:
        return null;
    }
    throw Error(v(156, n.tag));
  }
  function uf(e2, n) {
    switch (Mi(n), n.tag) {
      case 1:
        return le2(n.type) && Cr(), e2 = n.flags, e2 & 65536 ? (n.flags = e2 & -65537 | 128, n) : null;
      case 3:
        return Kn(), M2(re), M2(J), Ai(), e2 = n.flags, (e2 & 65536) !== 0 && (e2 & 128) === 0 ? (n.flags = e2 & -65537 | 128, n) : null;
      case 5:
        return Vi(n), null;
      case 13:
        if (M2(O), e2 = n.memoizedState, e2 !== null && e2.dehydrated !== null) {
          if (n.alternate === null)
            throw Error(v(340));
          Qn();
        }
        return e2 = n.flags, e2 & 65536 ? (n.flags = e2 & -65537 | 128, n) : null;
      case 19:
        return M2(O), null;
      case 4:
        return Kn(), null;
      case 10:
        return Fi(n.type._context), null;
      case 22:
      case 23:
        return Ji(), null;
      case 24:
        return null;
      default:
        return null;
    }
  }
  var tr = false, Z2 = false, of = typeof WeakSet == "function" ? WeakSet : Set, w2 = null;
  function Rn(e2, n) {
    var t = e2.ref;
    if (t !== null)
      if (typeof t == "function")
        try {
          t(null);
        } catch (r) {
          I(e2, n, r);
        }
      else
        t.current = null;
  }
  function ui(e2, n, t) {
    try {
      t();
    } catch (r) {
      I(e2, n, r);
    }
  }
  var ro = false;
  function sf(e2, n) {
    if (Wl = wr, e2 = es(), Li(e2)) {
      if ("selectionStart" in e2)
        var t = { start: e2.selectionStart, end: e2.selectionEnd };
      else
        e: {
          t = (t = e2.ownerDocument) && t.defaultView || window;
          var r = t.getSelection && t.getSelection();
          if (r && r.rangeCount !== 0) {
            t = r.anchorNode;
            var l = r.anchorOffset, i = r.focusNode;
            r = r.focusOffset;
            try {
              t.nodeType, i.nodeType;
            } catch {
              t = null;
              break e;
            }
            var u = 0, o = -1, s = -1, d = 0, m = 0, h2 = e2, p = null;
            n:
              for (; ; ) {
                for (var g; h2 !== t || l !== 0 && h2.nodeType !== 3 || (o = u + l), h2 !== i || r !== 0 && h2.nodeType !== 3 || (s = u + r), h2.nodeType === 3 && (u += h2.nodeValue.length), (g = h2.firstChild) !== null; )
                  p = h2, h2 = g;
                for (; ; ) {
                  if (h2 === e2)
                    break n;
                  if (p === t && ++d === l && (o = u), p === i && ++m === r && (s = u), (g = h2.nextSibling) !== null)
                    break;
                  h2 = p, p = h2.parentNode;
                }
                h2 = g;
              }
            t = o === -1 || s === -1 ? null : { start: o, end: s };
          } else
            t = null;
        }
      t = t || { start: 0, end: 0 };
    } else
      t = null;
    for (Ql = { focusedElem: e2, selectionRange: t }, wr = false, w2 = n; w2 !== null; )
      if (n = w2, e2 = n.child, (n.subtreeFlags & 1028) !== 0 && e2 !== null)
        e2.return = n, w2 = e2;
      else
        for (; w2 !== null; ) {
          n = w2;
          try {
            var S2 = n.alternate;
            if ((n.flags & 1024) !== 0)
              switch (n.tag) {
                case 0:
                case 11:
                case 15:
                  break;
                case 1:
                  if (S2 !== null) {
                    var k2 = S2.memoizedProps, j = S2.memoizedState, c = n.stateNode, a = c.getSnapshotBeforeUpdate(n.elementType === n.type ? k2 : we3(n.type, k2), j);
                    c.__reactInternalSnapshotBeforeUpdate = a;
                  }
                  break;
                case 3:
                  var f = n.stateNode.containerInfo;
                  f.nodeType === 1 ? f.textContent = "" : f.nodeType === 9 && f.documentElement && f.removeChild(f.documentElement);
                  break;
                case 5:
                case 6:
                case 4:
                case 17:
                  break;
                default:
                  throw Error(v(163));
              }
          } catch (y) {
            I(n, n.return, y);
          }
          if (e2 = n.sibling, e2 !== null) {
            e2.return = n.return, w2 = e2;
            break;
          }
          w2 = n.return;
        }
    return S2 = ro, ro = false, S2;
  }
  function ht(e2, n, t) {
    var r = n.updateQueue;
    if (r = r !== null ? r.lastEffect : null, r !== null) {
      var l = r = r.next;
      do {
        if ((l.tag & e2) === e2) {
          var i = l.destroy;
          l.destroy = void 0, i !== void 0 && ui(n, t, i);
        }
        l = l.next;
      } while (l !== r);
    }
  }
  function Kr(e2, n) {
    if (n = n.updateQueue, n = n !== null ? n.lastEffect : null, n !== null) {
      var t = n = n.next;
      do {
        if ((t.tag & e2) === e2) {
          var r = t.create;
          t.destroy = r();
        }
        t = t.next;
      } while (t !== n);
    }
  }
  function oi(e2) {
    var n = e2.ref;
    if (n !== null) {
      var t = e2.stateNode;
      switch (e2.tag) {
        case 5:
          e2 = t;
          break;
        default:
          e2 = t;
      }
      typeof n == "function" ? n(e2) : n.current = e2;
    }
  }
  function Js(e2) {
    var n = e2.alternate;
    n !== null && (e2.alternate = null, Js(n)), e2.child = null, e2.deletions = null, e2.sibling = null, e2.tag === 5 && (n = e2.stateNode, n !== null && (delete n[ze2], delete n[Pt], delete n[Yl], delete n[Wc], delete n[Qc])), e2.stateNode = null, e2.return = null, e2.dependencies = null, e2.memoizedProps = null, e2.memoizedState = null, e2.pendingProps = null, e2.stateNode = null, e2.updateQueue = null;
  }
  function qs(e2) {
    return e2.tag === 5 || e2.tag === 3 || e2.tag === 4;
  }
  function lo(e2) {
    e:
      for (; ; ) {
        for (; e2.sibling === null; ) {
          if (e2.return === null || qs(e2.return))
            return null;
          e2 = e2.return;
        }
        for (e2.sibling.return = e2.return, e2 = e2.sibling; e2.tag !== 5 && e2.tag !== 6 && e2.tag !== 18; ) {
          if (e2.flags & 2 || e2.child === null || e2.tag === 4)
            continue e;
          e2.child.return = e2, e2 = e2.child;
        }
        if (!(e2.flags & 2))
          return e2.stateNode;
      }
  }
  function si(e2, n, t) {
    var r = e2.tag;
    if (r === 5 || r === 6)
      e2 = e2.stateNode, n ? t.nodeType === 8 ? t.parentNode.insertBefore(e2, n) : t.insertBefore(e2, n) : (t.nodeType === 8 ? (n = t.parentNode, n.insertBefore(e2, t)) : (n = t, n.appendChild(e2)), t = t._reactRootContainer, t != null || n.onclick !== null || (n.onclick = Er));
    else if (r !== 4 && (e2 = e2.child, e2 !== null))
      for (si(e2, n, t), e2 = e2.sibling; e2 !== null; )
        si(e2, n, t), e2 = e2.sibling;
  }
  function ai(e2, n, t) {
    var r = e2.tag;
    if (r === 5 || r === 6)
      e2 = e2.stateNode, n ? t.insertBefore(e2, n) : t.appendChild(e2);
    else if (r !== 4 && (e2 = e2.child, e2 !== null))
      for (ai(e2, n, t), e2 = e2.sibling; e2 !== null; )
        ai(e2, n, t), e2 = e2.sibling;
  }
  var $2 = null, Se2 = false;
  function Be2(e2, n, t) {
    for (t = t.child; t !== null; )
      bs(e2, n, t), t = t.sibling;
  }
  function bs(e2, n, t) {
    if (Pe3 && typeof Pe3.onCommitFiberUnmount == "function")
      try {
        Pe3.onCommitFiberUnmount(Ur, t);
      } catch {
      }
    switch (t.tag) {
      case 5:
        Z2 || Rn(t, n);
      case 6:
        var r = $2, l = Se2;
        $2 = null, Be2(e2, n, t), $2 = r, Se2 = l, $2 !== null && (Se2 ? (e2 = $2, t = t.stateNode, e2.nodeType === 8 ? e2.parentNode.removeChild(t) : e2.removeChild(t)) : $2.removeChild(t.stateNode));
        break;
      case 18:
        $2 !== null && (Se2 ? (e2 = $2, t = t.stateNode, e2.nodeType === 8 ? dl(e2.parentNode, t) : e2.nodeType === 1 && dl(e2, t), Ct(e2)) : dl($2, t.stateNode));
        break;
      case 4:
        r = $2, l = Se2, $2 = t.stateNode.containerInfo, Se2 = true, Be2(e2, n, t), $2 = r, Se2 = l;
        break;
      case 0:
      case 11:
      case 14:
      case 15:
        if (!Z2 && (r = t.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
          l = r = r.next;
          do {
            var i = l, u = i.destroy;
            i = i.tag, u !== void 0 && ((i & 2) !== 0 || (i & 4) !== 0) && ui(t, n, u), l = l.next;
          } while (l !== r);
        }
        Be2(e2, n, t);
        break;
      case 1:
        if (!Z2 && (Rn(t, n), r = t.stateNode, typeof r.componentWillUnmount == "function"))
          try {
            r.props = t.memoizedProps, r.state = t.memoizedState, r.componentWillUnmount();
          } catch (o) {
            I(t, n, o);
          }
        Be2(e2, n, t);
        break;
      case 21:
        Be2(e2, n, t);
        break;
      case 22:
        t.mode & 1 ? (Z2 = (r = Z2) || t.memoizedState !== null, Be2(e2, n, t), Z2 = r) : Be2(e2, n, t);
        break;
      default:
        Be2(e2, n, t);
    }
  }
  function io(e2) {
    var n = e2.updateQueue;
    if (n !== null) {
      e2.updateQueue = null;
      var t = e2.stateNode;
      t === null && (t = e2.stateNode = new of()), n.forEach(function(r) {
        var l = yf.bind(null, e2, r);
        t.has(r) || (t.add(r), r.then(l, l));
      });
    }
  }
  function ge3(e2, n) {
    var t = n.deletions;
    if (t !== null)
      for (var r = 0; r < t.length; r++) {
        var l = t[r];
        try {
          var i = e2, u = n, o = u;
          e:
            for (; o !== null; ) {
              switch (o.tag) {
                case 5:
                  $2 = o.stateNode, Se2 = false;
                  break e;
                case 3:
                  $2 = o.stateNode.containerInfo, Se2 = true;
                  break e;
                case 4:
                  $2 = o.stateNode.containerInfo, Se2 = true;
                  break e;
              }
              o = o.return;
            }
          if ($2 === null)
            throw Error(v(160));
          bs(i, u, l), $2 = null, Se2 = false;
          var s = l.alternate;
          s !== null && (s.return = null), l.return = null;
        } catch (d) {
          I(l, n, d);
        }
      }
    if (n.subtreeFlags & 12854)
      for (n = n.child; n !== null; )
        ea(n, e2), n = n.sibling;
  }
  function ea(e2, n) {
    var t = e2.alternate, r = e2.flags;
    switch (e2.tag) {
      case 0:
      case 11:
      case 14:
      case 15:
        if (ge3(n, e2), Ne2(e2), r & 4) {
          try {
            ht(3, e2, e2.return), Kr(3, e2);
          } catch (k2) {
            I(e2, e2.return, k2);
          }
          try {
            ht(5, e2, e2.return);
          } catch (k2) {
            I(e2, e2.return, k2);
          }
        }
        break;
      case 1:
        ge3(n, e2), Ne2(e2), r & 512 && t !== null && Rn(t, t.return);
        break;
      case 5:
        if (ge3(n, e2), Ne2(e2), r & 512 && t !== null && Rn(t, t.return), e2.flags & 32) {
          var l = e2.stateNode;
          try {
            wt(l, "");
          } catch (k2) {
            I(e2, e2.return, k2);
          }
        }
        if (r & 4 && (l = e2.stateNode, l != null)) {
          var i = e2.memoizedProps, u = t !== null ? t.memoizedProps : i, o = e2.type, s = e2.updateQueue;
          if (e2.updateQueue = null, s !== null)
            try {
              o === "input" && i.type === "radio" && i.name != null && ko(l, i), Ol(o, u);
              var d = Ol(o, i);
              for (u = 0; u < s.length; u += 2) {
                var m = s[u], h2 = s[u + 1];
                m === "style" ? _o(l, h2) : m === "dangerouslySetInnerHTML" ? xo(l, h2) : m === "children" ? wt(l, h2) : vi(l, m, h2, d);
              }
              switch (o) {
                case "input":
                  Pl(l, i);
                  break;
                case "textarea":
                  Eo(l, i);
                  break;
                case "select":
                  var p = l._wrapperState.wasMultiple;
                  l._wrapperState.wasMultiple = !!i.multiple;
                  var g = i.value;
                  g != null ? In(l, !!i.multiple, g, false) : p !== !!i.multiple && (i.defaultValue != null ? In(l, !!i.multiple, i.defaultValue, true) : In(l, !!i.multiple, i.multiple ? [] : "", false));
              }
              l[Pt] = i;
            } catch (k2) {
              I(e2, e2.return, k2);
            }
        }
        break;
      case 6:
        if (ge3(n, e2), Ne2(e2), r & 4) {
          if (e2.stateNode === null)
            throw Error(v(162));
          l = e2.stateNode, i = e2.memoizedProps;
          try {
            l.nodeValue = i;
          } catch (k2) {
            I(e2, e2.return, k2);
          }
        }
        break;
      case 3:
        if (ge3(n, e2), Ne2(e2), r & 4 && t !== null && t.memoizedState.isDehydrated)
          try {
            Ct(n.containerInfo);
          } catch (k2) {
            I(e2, e2.return, k2);
          }
        break;
      case 4:
        ge3(n, e2), Ne2(e2);
        break;
      case 13:
        ge3(n, e2), Ne2(e2), l = e2.child, l.flags & 8192 && (i = l.memoizedState !== null, l.stateNode.isHidden = i, !i || l.alternate !== null && l.alternate.memoizedState !== null || (Gi = U3())), r & 4 && io(e2);
        break;
      case 22:
        if (m = t !== null && t.memoizedState !== null, e2.mode & 1 ? (Z2 = (d = Z2) || m, ge3(n, e2), Z2 = d) : ge3(n, e2), Ne2(e2), r & 8192) {
          if (d = e2.memoizedState !== null, (e2.stateNode.isHidden = d) && !m && (e2.mode & 1) !== 0)
            for (w2 = e2, m = e2.child; m !== null; ) {
              for (h2 = w2 = m; w2 !== null; ) {
                switch (p = w2, g = p.child, p.tag) {
                  case 0:
                  case 11:
                  case 14:
                  case 15:
                    ht(4, p, p.return);
                    break;
                  case 1:
                    Rn(p, p.return);
                    var S2 = p.stateNode;
                    if (typeof S2.componentWillUnmount == "function") {
                      r = p, t = p.return;
                      try {
                        n = r, S2.props = n.memoizedProps, S2.state = n.memoizedState, S2.componentWillUnmount();
                      } catch (k2) {
                        I(r, t, k2);
                      }
                    }
                    break;
                  case 5:
                    Rn(p, p.return);
                    break;
                  case 22:
                    if (p.memoizedState !== null) {
                      oo(h2);
                      continue;
                    }
                }
                g !== null ? (g.return = p, w2 = g) : oo(h2);
              }
              m = m.sibling;
            }
          e:
            for (m = null, h2 = e2; ; ) {
              if (h2.tag === 5) {
                if (m === null) {
                  m = h2;
                  try {
                    l = h2.stateNode, d ? (i = l.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (o = h2.stateNode, s = h2.memoizedProps.style, u = s != null && s.hasOwnProperty("display") ? s.display : null, o.style.display = No("display", u));
                  } catch (k2) {
                    I(e2, e2.return, k2);
                  }
                }
              } else if (h2.tag === 6) {
                if (m === null)
                  try {
                    h2.stateNode.nodeValue = d ? "" : h2.memoizedProps;
                  } catch (k2) {
                    I(e2, e2.return, k2);
                  }
              } else if ((h2.tag !== 22 && h2.tag !== 23 || h2.memoizedState === null || h2 === e2) && h2.child !== null) {
                h2.child.return = h2, h2 = h2.child;
                continue;
              }
              if (h2 === e2)
                break e;
              for (; h2.sibling === null; ) {
                if (h2.return === null || h2.return === e2)
                  break e;
                m === h2 && (m = null), h2 = h2.return;
              }
              m === h2 && (m = null), h2.sibling.return = h2.return, h2 = h2.sibling;
            }
        }
        break;
      case 19:
        ge3(n, e2), Ne2(e2), r & 4 && io(e2);
        break;
      case 21:
        break;
      default:
        ge3(n, e2), Ne2(e2);
    }
  }
  function Ne2(e2) {
    var n = e2.flags;
    if (n & 2) {
      try {
        e: {
          for (var t = e2.return; t !== null; ) {
            if (qs(t)) {
              var r = t;
              break e;
            }
            t = t.return;
          }
          throw Error(v(160));
        }
        switch (r.tag) {
          case 5:
            var l = r.stateNode;
            r.flags & 32 && (wt(l, ""), r.flags &= -33);
            var i = lo(e2);
            ai(e2, i, l);
            break;
          case 3:
          case 4:
            var u = r.stateNode.containerInfo, o = lo(e2);
            si(e2, o, u);
            break;
          default:
            throw Error(v(161));
        }
      } catch (s) {
        I(e2, e2.return, s);
      }
      e2.flags &= -3;
    }
    n & 4096 && (e2.flags &= -4097);
  }
  function af(e2, n, t) {
    w2 = e2, na(e2, n, t);
  }
  function na(e2, n, t) {
    for (var r = (e2.mode & 1) !== 0; w2 !== null; ) {
      var l = w2, i = l.child;
      if (l.tag === 22 && r) {
        var u = l.memoizedState !== null || tr;
        if (!u) {
          var o = l.alternate, s = o !== null && o.memoizedState !== null || Z2;
          o = tr;
          var d = Z2;
          if (tr = u, (Z2 = s) && !d)
            for (w2 = l; w2 !== null; )
              u = w2, s = u.child, u.tag === 22 && u.memoizedState !== null ? so(l) : s !== null ? (s.return = u, w2 = s) : so(l);
          for (; i !== null; )
            w2 = i, na(i, n, t), i = i.sibling;
          w2 = l, tr = o, Z2 = d;
        }
        uo(e2, n, t);
      } else
        (l.subtreeFlags & 8772) !== 0 && i !== null ? (i.return = l, w2 = i) : uo(e2, n, t);
    }
  }
  function uo(e2) {
    for (; w2 !== null; ) {
      var n = w2;
      if ((n.flags & 8772) !== 0) {
        var t = n.alternate;
        try {
          if ((n.flags & 8772) !== 0)
            switch (n.tag) {
              case 0:
              case 11:
              case 15:
                Z2 || Kr(5, n);
                break;
              case 1:
                var r = n.stateNode;
                if (n.flags & 4 && !Z2)
                  if (t === null)
                    r.componentDidMount();
                  else {
                    var l = n.elementType === n.type ? t.memoizedProps : we3(n.type, t.memoizedProps);
                    r.componentDidUpdate(l, t.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
                  }
                var i = n.updateQueue;
                i !== null && Wu(n, i, r);
                break;
              case 3:
                var u = n.updateQueue;
                if (u !== null) {
                  if (t = null, n.child !== null)
                    switch (n.child.tag) {
                      case 5:
                        t = n.child.stateNode;
                        break;
                      case 1:
                        t = n.child.stateNode;
                    }
                  Wu(n, u, t);
                }
                break;
              case 5:
                var o = n.stateNode;
                if (t === null && n.flags & 4) {
                  t = o;
                  var s = n.memoizedProps;
                  switch (n.type) {
                    case "button":
                    case "input":
                    case "select":
                    case "textarea":
                      s.autoFocus && t.focus();
                      break;
                    case "img":
                      s.src && (t.src = s.src);
                  }
                }
                break;
              case 6:
                break;
              case 4:
                break;
              case 12:
                break;
              case 13:
                if (n.memoizedState === null) {
                  var d = n.alternate;
                  if (d !== null) {
                    var m = d.memoizedState;
                    if (m !== null) {
                      var h2 = m.dehydrated;
                      h2 !== null && Ct(h2);
                    }
                  }
                }
                break;
              case 19:
              case 17:
              case 21:
              case 22:
              case 23:
              case 25:
                break;
              default:
                throw Error(v(163));
            }
          Z2 || n.flags & 512 && oi(n);
        } catch (p) {
          I(n, n.return, p);
        }
      }
      if (n === e2) {
        w2 = null;
        break;
      }
      if (t = n.sibling, t !== null) {
        t.return = n.return, w2 = t;
        break;
      }
      w2 = n.return;
    }
  }
  function oo(e2) {
    for (; w2 !== null; ) {
      var n = w2;
      if (n === e2) {
        w2 = null;
        break;
      }
      var t = n.sibling;
      if (t !== null) {
        t.return = n.return, w2 = t;
        break;
      }
      w2 = n.return;
    }
  }
  function so(e2) {
    for (; w2 !== null; ) {
      var n = w2;
      try {
        switch (n.tag) {
          case 0:
          case 11:
          case 15:
            var t = n.return;
            try {
              Kr(4, n);
            } catch (s) {
              I(n, t, s);
            }
            break;
          case 1:
            var r = n.stateNode;
            if (typeof r.componentDidMount == "function") {
              var l = n.return;
              try {
                r.componentDidMount();
              } catch (s) {
                I(n, l, s);
              }
            }
            var i = n.return;
            try {
              oi(n);
            } catch (s) {
              I(n, i, s);
            }
            break;
          case 5:
            var u = n.return;
            try {
              oi(n);
            } catch (s) {
              I(n, u, s);
            }
        }
      } catch (s) {
        I(n, n.return, s);
      }
      if (n === e2) {
        w2 = null;
        break;
      }
      var o = n.sibling;
      if (o !== null) {
        o.return = n.return, w2 = o;
        break;
      }
      w2 = n.return;
    }
  }
  var cf = Math.ceil, Or = Ve2.ReactCurrentDispatcher, Yi = Ve2.ReactCurrentOwner, he3 = Ve2.ReactCurrentBatchConfig, _ = 0, Q = null, V3 = null, K2 = 0, ue2 = 0, Fn = un(0), B3 = 0, Rt = null, gn = 0, Yr = 0, Xi = 0, vt = null, ne2 = null, Gi = 0, Xn = 1 / 0, Te2 = null, Rr = false, ci = null, be3 = null, rr = false, Ye = null, Fr = 0, yt = 0, fi = null, fr = -1, dr = 0;
  function b() {
    return (_ & 6) !== 0 ? U3() : fr !== -1 ? fr : fr = U3();
  }
  function en(e2) {
    return (e2.mode & 1) === 0 ? 1 : (_ & 2) !== 0 && K2 !== 0 ? K2 & -K2 : Kc.transition !== null ? (dr === 0 && (dr = Uo()), dr) : (e2 = P, e2 !== 0 || (e2 = window.event, e2 = e2 === void 0 ? 16 : $o(e2.type)), e2);
  }
  function Ce2(e2, n, t, r) {
    if (50 < yt)
      throw yt = 0, fi = null, Error(v(185));
    Ft(e2, t, r), ((_ & 2) === 0 || e2 !== Q) && (e2 === Q && ((_ & 2) === 0 && (Yr |= t), B3 === 4 && $e2(e2, K2)), ie(e2, r), t === 1 && _ === 0 && (n.mode & 1) === 0 && (Xn = U3() + 500, Wr && on()));
  }
  function ie(e2, n) {
    var t = e2.callbackNode;
    Xa(e2, n);
    var r = gr(e2, e2 === Q ? K2 : 0);
    if (r === 0)
      t !== null && vu(t), e2.callbackNode = null, e2.callbackPriority = 0;
    else if (n = r & -r, e2.callbackPriority !== n) {
      if (t != null && vu(t), n === 1)
        e2.tag === 0 ? $c(ao.bind(null, e2)) : cs(ao.bind(null, e2)), Bc(function() {
          (_ & 6) === 0 && on();
        }), t = null;
      else {
        switch (Vo(r)) {
          case 1:
            t = ki;
            break;
          case 4:
            t = Io;
            break;
          case 16:
            t = yr;
            break;
          case 536870912:
            t = jo;
            break;
          default:
            t = yr;
        }
        t = aa(t, ta.bind(null, e2));
      }
      e2.callbackPriority = n, e2.callbackNode = t;
    }
  }
  function ta(e2, n) {
    if (fr = -1, dr = 0, (_ & 6) !== 0)
      throw Error(v(327));
    var t = e2.callbackNode;
    if (Bn() && e2.callbackNode !== t)
      return null;
    var r = gr(e2, e2 === Q ? K2 : 0);
    if (r === 0)
      return null;
    if ((r & 30) !== 0 || (r & e2.expiredLanes) !== 0 || n)
      n = Ir(e2, r);
    else {
      n = r;
      var l = _;
      _ |= 2;
      var i = la();
      (Q !== e2 || K2 !== n) && (Te2 = null, Xn = U3() + 500, pn(e2, n));
      do
        try {
          pf();
          break;
        } catch (o) {
          ra(e2, o);
        }
      while (true);
      Ri(), Or.current = i, _ = l, V3 !== null ? n = 0 : (Q = null, K2 = 0, n = B3);
    }
    if (n !== 0) {
      if (n === 2 && (l = Ul(e2), l !== 0 && (r = l, n = di(e2, l))), n === 1)
        throw t = Rt, pn(e2, 0), $e2(e2, r), ie(e2, U3()), t;
      if (n === 6)
        $e2(e2, r);
      else {
        if (l = e2.current.alternate, (r & 30) === 0 && !ff(l) && (n = Ir(e2, r), n === 2 && (i = Ul(e2), i !== 0 && (r = i, n = di(e2, i))), n === 1))
          throw t = Rt, pn(e2, 0), $e2(e2, r), ie(e2, U3()), t;
        switch (e2.finishedWork = l, e2.finishedLanes = r, n) {
          case 0:
          case 1:
            throw Error(v(345));
          case 2:
            an(e2, ne2, Te2);
            break;
          case 3:
            if ($e2(e2, r), (r & 130023424) === r && (n = Gi + 500 - U3(), 10 < n)) {
              if (gr(e2, 0) !== 0)
                break;
              if (l = e2.suspendedLanes, (l & r) !== r) {
                b(), e2.pingedLanes |= e2.suspendedLanes & l;
                break;
              }
              e2.timeoutHandle = Kl(an.bind(null, e2, ne2, Te2), n);
              break;
            }
            an(e2, ne2, Te2);
            break;
          case 4:
            if ($e2(e2, r), (r & 4194240) === r)
              break;
            for (n = e2.eventTimes, l = -1; 0 < r; ) {
              var u = 31 - Ee2(r);
              i = 1 << u, u = n[u], u > l && (l = u), r &= ~i;
            }
            if (r = l, r = U3() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * cf(r / 1960)) - r, 10 < r) {
              e2.timeoutHandle = Kl(an.bind(null, e2, ne2, Te2), r);
              break;
            }
            an(e2, ne2, Te2);
            break;
          case 5:
            an(e2, ne2, Te2);
            break;
          default:
            throw Error(v(329));
        }
      }
    }
    return ie(e2, U3()), e2.callbackNode === t ? ta.bind(null, e2) : null;
  }
  function di(e2, n) {
    var t = vt;
    return e2.current.memoizedState.isDehydrated && (pn(e2, n).flags |= 256), e2 = Ir(e2, n), e2 !== 2 && (n = ne2, ne2 = t, n !== null && pi(n)), e2;
  }
  function pi(e2) {
    ne2 === null ? ne2 = e2 : ne2.push.apply(ne2, e2);
  }
  function ff(e2) {
    for (var n = e2; ; ) {
      if (n.flags & 16384) {
        var t = n.updateQueue;
        if (t !== null && (t = t.stores, t !== null))
          for (var r = 0; r < t.length; r++) {
            var l = t[r], i = l.getSnapshot;
            l = l.value;
            try {
              if (!xe3(i(), l))
                return false;
            } catch {
              return false;
            }
          }
      }
      if (t = n.child, n.subtreeFlags & 16384 && t !== null)
        t.return = n, n = t;
      else {
        if (n === e2)
          break;
        for (; n.sibling === null; ) {
          if (n.return === null || n.return === e2)
            return true;
          n = n.return;
        }
        n.sibling.return = n.return, n = n.sibling;
      }
    }
    return true;
  }
  function $e2(e2, n) {
    for (n &= ~Xi, n &= ~Yr, e2.suspendedLanes |= n, e2.pingedLanes &= ~n, e2 = e2.expirationTimes; 0 < n; ) {
      var t = 31 - Ee2(n), r = 1 << t;
      e2[t] = -1, n &= ~r;
    }
  }
  function ao(e2) {
    if ((_ & 6) !== 0)
      throw Error(v(327));
    Bn();
    var n = gr(e2, 0);
    if ((n & 1) === 0)
      return ie(e2, U3()), null;
    var t = Ir(e2, n);
    if (e2.tag !== 0 && t === 2) {
      var r = Ul(e2);
      r !== 0 && (n = r, t = di(e2, r));
    }
    if (t === 1)
      throw t = Rt, pn(e2, 0), $e2(e2, n), ie(e2, U3()), t;
    if (t === 6)
      throw Error(v(345));
    return e2.finishedWork = e2.current.alternate, e2.finishedLanes = n, an(e2, ne2, Te2), ie(e2, U3()), null;
  }
  function Zi(e2, n) {
    var t = _;
    _ |= 1;
    try {
      return e2(n);
    } finally {
      _ = t, _ === 0 && (Xn = U3() + 500, Wr && on());
    }
  }
  function wn(e2) {
    Ye !== null && Ye.tag === 0 && (_ & 6) === 0 && Bn();
    var n = _;
    _ |= 1;
    var t = he3.transition, r = P;
    try {
      if (he3.transition = null, P = 1, e2)
        return e2();
    } finally {
      P = r, he3.transition = t, _ = n, (_ & 6) === 0 && on();
    }
  }
  function Ji() {
    ue2 = Fn.current, M2(Fn);
  }
  function pn(e2, n) {
    e2.finishedWork = null, e2.finishedLanes = 0;
    var t = e2.timeoutHandle;
    if (t !== -1 && (e2.timeoutHandle = -1, Ac(t)), V3 !== null)
      for (t = V3.return; t !== null; ) {
        var r = t;
        switch (Mi(r), r.tag) {
          case 1:
            r = r.type.childContextTypes, r != null && Cr();
            break;
          case 3:
            Kn(), M2(re), M2(J), Ai();
            break;
          case 5:
            Vi(r);
            break;
          case 4:
            Kn();
            break;
          case 13:
            M2(O);
            break;
          case 19:
            M2(O);
            break;
          case 10:
            Fi(r.type._context);
            break;
          case 22:
          case 23:
            Ji();
        }
        t = t.return;
      }
    if (Q = e2, V3 = e2 = nn(e2.current, null), K2 = ue2 = n, B3 = 0, Rt = null, Xi = Yr = gn = 0, ne2 = vt = null, fn !== null) {
      for (n = 0; n < fn.length; n++)
        if (t = fn[n], r = t.interleaved, r !== null) {
          t.interleaved = null;
          var l = r.next, i = t.pending;
          if (i !== null) {
            var u = i.next;
            i.next = l, r.next = u;
          }
          t.pending = r;
        }
      fn = null;
    }
    return e2;
  }
  function ra(e2, n) {
    do {
      var t = V3;
      try {
        if (Ri(), sr.current = Dr, Mr) {
          for (var r = R.memoizedState; r !== null; ) {
            var l = r.queue;
            l !== null && (l.pending = null), r = r.next;
          }
          Mr = false;
        }
        if (yn = 0, W = A2 = R = null, mt = false, Mt = 0, Yi.current = null, t === null || t.return === null) {
          B3 = 1, Rt = n, V3 = null;
          break;
        }
        e: {
          var i = e2, u = t.return, o = t, s = n;
          if (n = K2, o.flags |= 32768, s !== null && typeof s == "object" && typeof s.then == "function") {
            var d = s, m = o, h2 = m.tag;
            if ((m.mode & 1) === 0 && (h2 === 0 || h2 === 11 || h2 === 15)) {
              var p = m.alternate;
              p ? (m.updateQueue = p.updateQueue, m.memoizedState = p.memoizedState, m.lanes = p.lanes) : (m.updateQueue = null, m.memoizedState = null);
            }
            var g = Zu(u);
            if (g !== null) {
              g.flags &= -257, Ju(g, u, o, i, n), g.mode & 1 && Gu(i, d, n), n = g, s = d;
              var S2 = n.updateQueue;
              if (S2 === null) {
                var k2 = new Set();
                k2.add(s), n.updateQueue = k2;
              } else
                S2.add(s);
              break e;
            } else {
              if ((n & 1) === 0) {
                Gu(i, d, n), qi();
                break e;
              }
              s = Error(v(426));
            }
          } else if (D2 && o.mode & 1) {
            var j = Zu(u);
            if (j !== null) {
              (j.flags & 65536) === 0 && (j.flags |= 256), Ju(j, u, o, i, n), Di(Yn(s, o));
              break e;
            }
          }
          i = s = Yn(s, o), B3 !== 4 && (B3 = 2), vt === null ? vt = [i] : vt.push(i), i = u;
          do {
            switch (i.tag) {
              case 3:
                i.flags |= 65536, n &= -n, i.lanes |= n;
                var c = As(i, s, n);
                Hu(i, c);
                break e;
              case 1:
                o = s;
                var a = i.type, f = i.stateNode;
                if ((i.flags & 128) === 0 && (typeof a.getDerivedStateFromError == "function" || f !== null && typeof f.componentDidCatch == "function" && (be3 === null || !be3.has(f)))) {
                  i.flags |= 65536, n &= -n, i.lanes |= n;
                  var y = Bs(i, o, n);
                  Hu(i, y);
                  break e;
                }
            }
            i = i.return;
          } while (i !== null);
        }
        ua(t);
      } catch (E) {
        n = E, V3 === t && t !== null && (V3 = t = t.return);
        continue;
      }
      break;
    } while (true);
  }
  function la() {
    var e2 = Or.current;
    return Or.current = Dr, e2 === null ? Dr : e2;
  }
  function qi() {
    (B3 === 0 || B3 === 3 || B3 === 2) && (B3 = 4), Q === null || (gn & 268435455) === 0 && (Yr & 268435455) === 0 || $e2(Q, K2);
  }
  function Ir(e2, n) {
    var t = _;
    _ |= 2;
    var r = la();
    (Q !== e2 || K2 !== n) && (Te2 = null, pn(e2, n));
    do
      try {
        df();
        break;
      } catch (l) {
        ra(e2, l);
      }
    while (true);
    if (Ri(), _ = t, Or.current = r, V3 !== null)
      throw Error(v(261));
    return Q = null, K2 = 0, B3;
  }
  function df() {
    for (; V3 !== null; )
      ia(V3);
  }
  function pf() {
    for (; V3 !== null && !Va(); )
      ia(V3);
  }
  function ia(e2) {
    var n = sa(e2.alternate, e2, ue2);
    e2.memoizedProps = e2.pendingProps, n === null ? ua(e2) : V3 = n, Yi.current = null;
  }
  function ua(e2) {
    var n = e2;
    do {
      var t = n.alternate;
      if (e2 = n.return, (n.flags & 32768) === 0) {
        if (t = lf(t, n, ue2), t !== null) {
          V3 = t;
          return;
        }
      } else {
        if (t = uf(t, n), t !== null) {
          t.flags &= 32767, V3 = t;
          return;
        }
        if (e2 !== null)
          e2.flags |= 32768, e2.subtreeFlags = 0, e2.deletions = null;
        else {
          B3 = 6, V3 = null;
          return;
        }
      }
      if (n = n.sibling, n !== null) {
        V3 = n;
        return;
      }
      V3 = n = e2;
    } while (n !== null);
    B3 === 0 && (B3 = 5);
  }
  function an(e2, n, t) {
    var r = P, l = he3.transition;
    try {
      he3.transition = null, P = 1, mf(e2, n, t, r);
    } finally {
      he3.transition = l, P = r;
    }
    return null;
  }
  function mf(e2, n, t, r) {
    do
      Bn();
    while (Ye !== null);
    if ((_ & 6) !== 0)
      throw Error(v(327));
    t = e2.finishedWork;
    var l = e2.finishedLanes;
    if (t === null)
      return null;
    if (e2.finishedWork = null, e2.finishedLanes = 0, t === e2.current)
      throw Error(v(177));
    e2.callbackNode = null, e2.callbackPriority = 0;
    var i = t.lanes | t.childLanes;
    if (Ga(e2, i), e2 === Q && (V3 = Q = null, K2 = 0), (t.subtreeFlags & 2064) === 0 && (t.flags & 2064) === 0 || rr || (rr = true, aa(yr, function() {
      return Bn(), null;
    })), i = (t.flags & 15990) !== 0, (t.subtreeFlags & 15990) !== 0 || i) {
      i = he3.transition, he3.transition = null;
      var u = P;
      P = 1;
      var o = _;
      _ |= 4, Yi.current = null, sf(e2, t), ea(t, e2), Fc(Ql), wr = !!Wl, Ql = Wl = null, e2.current = t, af(t, e2, l), Aa(), _ = o, P = u, he3.transition = i;
    } else
      e2.current = t;
    if (rr && (rr = false, Ye = e2, Fr = l), i = e2.pendingLanes, i === 0 && (be3 = null), Wa(t.stateNode, r), ie(e2, U3()), n !== null)
      for (r = e2.onRecoverableError, t = 0; t < n.length; t++)
        l = n[t], r(l.value, { componentStack: l.stack, digest: l.digest });
    if (Rr)
      throw Rr = false, e2 = ci, ci = null, e2;
    return (Fr & 1) !== 0 && e2.tag !== 0 && Bn(), i = e2.pendingLanes, (i & 1) !== 0 ? e2 === fi ? yt++ : (yt = 0, fi = e2) : yt = 0, on(), null;
  }
  function Bn() {
    if (Ye !== null) {
      var e2 = Vo(Fr), n = he3.transition, t = P;
      try {
        if (he3.transition = null, P = 16 > e2 ? 16 : e2, Ye === null)
          var r = false;
        else {
          if (e2 = Ye, Ye = null, Fr = 0, (_ & 6) !== 0)
            throw Error(v(331));
          var l = _;
          for (_ |= 4, w2 = e2.current; w2 !== null; ) {
            var i = w2, u = i.child;
            if ((w2.flags & 16) !== 0) {
              var o = i.deletions;
              if (o !== null) {
                for (var s = 0; s < o.length; s++) {
                  var d = o[s];
                  for (w2 = d; w2 !== null; ) {
                    var m = w2;
                    switch (m.tag) {
                      case 0:
                      case 11:
                      case 15:
                        ht(8, m, i);
                    }
                    var h2 = m.child;
                    if (h2 !== null)
                      h2.return = m, w2 = h2;
                    else
                      for (; w2 !== null; ) {
                        m = w2;
                        var p = m.sibling, g = m.return;
                        if (Js(m), m === d) {
                          w2 = null;
                          break;
                        }
                        if (p !== null) {
                          p.return = g, w2 = p;
                          break;
                        }
                        w2 = g;
                      }
                  }
                }
                var S2 = i.alternate;
                if (S2 !== null) {
                  var k2 = S2.child;
                  if (k2 !== null) {
                    S2.child = null;
                    do {
                      var j = k2.sibling;
                      k2.sibling = null, k2 = j;
                    } while (k2 !== null);
                  }
                }
                w2 = i;
              }
            }
            if ((i.subtreeFlags & 2064) !== 0 && u !== null)
              u.return = i, w2 = u;
            else
              e:
                for (; w2 !== null; ) {
                  if (i = w2, (i.flags & 2048) !== 0)
                    switch (i.tag) {
                      case 0:
                      case 11:
                      case 15:
                        ht(9, i, i.return);
                    }
                  var c = i.sibling;
                  if (c !== null) {
                    c.return = i.return, w2 = c;
                    break e;
                  }
                  w2 = i.return;
                }
          }
          var a = e2.current;
          for (w2 = a; w2 !== null; ) {
            u = w2;
            var f = u.child;
            if ((u.subtreeFlags & 2064) !== 0 && f !== null)
              f.return = u, w2 = f;
            else
              e:
                for (u = a; w2 !== null; ) {
                  if (o = w2, (o.flags & 2048) !== 0)
                    try {
                      switch (o.tag) {
                        case 0:
                        case 11:
                        case 15:
                          Kr(9, o);
                      }
                    } catch (E) {
                      I(o, o.return, E);
                    }
                  if (o === u) {
                    w2 = null;
                    break e;
                  }
                  var y = o.sibling;
                  if (y !== null) {
                    y.return = o.return, w2 = y;
                    break e;
                  }
                  w2 = o.return;
                }
          }
          if (_ = l, on(), Pe3 && typeof Pe3.onPostCommitFiberRoot == "function")
            try {
              Pe3.onPostCommitFiberRoot(Ur, e2);
            } catch {
            }
          r = true;
        }
        return r;
      } finally {
        P = t, he3.transition = n;
      }
    }
    return false;
  }
  function co(e2, n, t) {
    n = Yn(t, n), n = As(e2, n, 1), e2 = qe2(e2, n, 1), n = b(), e2 !== null && (Ft(e2, 1, n), ie(e2, n));
  }
  function I(e2, n, t) {
    if (e2.tag === 3)
      co(e2, e2, t);
    else
      for (; n !== null; ) {
        if (n.tag === 3) {
          co(n, e2, t);
          break;
        } else if (n.tag === 1) {
          var r = n.stateNode;
          if (typeof n.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (be3 === null || !be3.has(r))) {
            e2 = Yn(t, e2), e2 = Bs(n, e2, 1), n = qe2(n, e2, 1), e2 = b(), n !== null && (Ft(n, 1, e2), ie(n, e2));
            break;
          }
        }
        n = n.return;
      }
  }
  function hf(e2, n, t) {
    var r = e2.pingCache;
    r !== null && r.delete(n), n = b(), e2.pingedLanes |= e2.suspendedLanes & t, Q === e2 && (K2 & t) === t && (B3 === 4 || B3 === 3 && (K2 & 130023424) === K2 && 500 > U3() - Gi ? pn(e2, 0) : Xi |= t), ie(e2, n);
  }
  function oa(e2, n) {
    n === 0 && ((e2.mode & 1) === 0 ? n = 1 : (n = Wt, Wt <<= 1, (Wt & 130023424) === 0 && (Wt = 4194304)));
    var t = b();
    e2 = je2(e2, n), e2 !== null && (Ft(e2, n, t), ie(e2, t));
  }
  function vf(e2) {
    var n = e2.memoizedState, t = 0;
    n !== null && (t = n.retryLane), oa(e2, t);
  }
  function yf(e2, n) {
    var t = 0;
    switch (e2.tag) {
      case 13:
        var r = e2.stateNode, l = e2.memoizedState;
        l !== null && (t = l.retryLane);
        break;
      case 19:
        r = e2.stateNode;
        break;
      default:
        throw Error(v(314));
    }
    r !== null && r.delete(n), oa(e2, t);
  }
  var sa;
  sa = function(e2, n, t) {
    if (e2 !== null)
      if (e2.memoizedProps !== n.pendingProps || re.current)
        te = true;
      else {
        if ((e2.lanes & t) === 0 && (n.flags & 128) === 0)
          return te = false, rf(e2, n, t);
        te = (e2.flags & 131072) !== 0;
      }
    else
      te = false, D2 && (n.flags & 1048576) !== 0 && fs(n, _r, n.index);
    switch (n.lanes = 0, n.tag) {
      case 2:
        var r = n.type;
        cr(e2, n), e2 = n.pendingProps;
        var l = Wn(n, J.current);
        An(n, t), l = Hi(null, n, r, e2, l, t);
        var i = Wi();
        return n.flags |= 1, typeof l == "object" && l !== null && typeof l.render == "function" && l.$$typeof === void 0 ? (n.tag = 1, n.memoizedState = null, n.updateQueue = null, le2(r) ? (i = true, xr(n)) : i = false, n.memoizedState = l.state !== null && l.state !== void 0 ? l.state : null, ji(n), l.updater = Qr, n.stateNode = l, l._reactInternals = n, bl(n, r, e2, t), n = ti(null, n, r, true, i, t)) : (n.tag = 0, D2 && i && Ti(n), q2(null, n, l, t), n = n.child), n;
      case 16:
        r = n.elementType;
        e: {
          switch (cr(e2, n), e2 = n.pendingProps, l = r._init, r = l(r._payload), n.type = r, l = n.tag = wf(r), e2 = we3(r, e2), l) {
            case 0:
              n = ni(null, n, r, e2, t);
              break e;
            case 1:
              n = eo(null, n, r, e2, t);
              break e;
            case 11:
              n = qu(null, n, r, e2, t);
              break e;
            case 14:
              n = bu(null, n, r, we3(r.type, e2), t);
              break e;
          }
          throw Error(v(306, r, ""));
        }
        return n;
      case 0:
        return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : we3(r, l), ni(e2, n, r, l, t);
      case 1:
        return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : we3(r, l), eo(e2, n, r, l, t);
      case 3:
        e: {
          if ($s(n), e2 === null)
            throw Error(v(387));
          r = n.pendingProps, i = n.memoizedState, l = i.element, hs(e2, n), Lr(n, r, null, t);
          var u = n.memoizedState;
          if (r = u.element, i.isDehydrated)
            if (i = { element: r, isDehydrated: false, cache: u.cache, pendingSuspenseBoundaries: u.pendingSuspenseBoundaries, transitions: u.transitions }, n.updateQueue.baseState = i, n.memoizedState = i, n.flags & 256) {
              l = Yn(Error(v(423)), n), n = no(e2, n, r, t, l);
              break e;
            } else if (r !== l) {
              l = Yn(Error(v(424)), n), n = no(e2, n, r, t, l);
              break e;
            } else
              for (oe2 = Je(n.stateNode.containerInfo.firstChild), se2 = n, D2 = true, ke3 = null, t = ws(n, null, r, t), n.child = t; t; )
                t.flags = t.flags & -3 | 4096, t = t.sibling;
          else {
            if (Qn(), r === l) {
              n = Ue2(e2, n, t);
              break e;
            }
            q2(e2, n, r, t);
          }
          n = n.child;
        }
        return n;
      case 5:
        return Ss(n), e2 === null && Zl(n), r = n.type, l = n.pendingProps, i = e2 !== null ? e2.memoizedProps : null, u = l.children, $l(r, l) ? u = null : i !== null && $l(r, i) && (n.flags |= 32), Qs(e2, n), q2(e2, n, u, t), n.child;
      case 6:
        return e2 === null && Zl(n), null;
      case 13:
        return Ks(e2, n, t);
      case 4:
        return Ui(n, n.stateNode.containerInfo), r = n.pendingProps, e2 === null ? n.child = $n(n, null, r, t) : q2(e2, n, r, t), n.child;
      case 11:
        return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : we3(r, l), qu(e2, n, r, l, t);
      case 7:
        return q2(e2, n, n.pendingProps, t), n.child;
      case 8:
        return q2(e2, n, n.pendingProps.children, t), n.child;
      case 12:
        return q2(e2, n, n.pendingProps.children, t), n.child;
      case 10:
        e: {
          if (r = n.type._context, l = n.pendingProps, i = n.memoizedProps, u = l.value, L(zr, r._currentValue), r._currentValue = u, i !== null)
            if (xe3(i.value, u)) {
              if (i.children === l.children && !re.current) {
                n = Ue2(e2, n, t);
                break e;
              }
            } else
              for (i = n.child, i !== null && (i.return = n); i !== null; ) {
                var o = i.dependencies;
                if (o !== null) {
                  u = i.child;
                  for (var s = o.firstContext; s !== null; ) {
                    if (s.context === r) {
                      if (i.tag === 1) {
                        s = Re2(-1, t & -t), s.tag = 2;
                        var d = i.updateQueue;
                        if (d !== null) {
                          d = d.shared;
                          var m = d.pending;
                          m === null ? s.next = s : (s.next = m.next, m.next = s), d.pending = s;
                        }
                      }
                      i.lanes |= t, s = i.alternate, s !== null && (s.lanes |= t), Jl(i.return, t, n), o.lanes |= t;
                      break;
                    }
                    s = s.next;
                  }
                } else if (i.tag === 10)
                  u = i.type === n.type ? null : i.child;
                else if (i.tag === 18) {
                  if (u = i.return, u === null)
                    throw Error(v(341));
                  u.lanes |= t, o = u.alternate, o !== null && (o.lanes |= t), Jl(u, t, n), u = i.sibling;
                } else
                  u = i.child;
                if (u !== null)
                  u.return = i;
                else
                  for (u = i; u !== null; ) {
                    if (u === n) {
                      u = null;
                      break;
                    }
                    if (i = u.sibling, i !== null) {
                      i.return = u.return, u = i;
                      break;
                    }
                    u = u.return;
                  }
                i = u;
              }
          q2(e2, n, l.children, t), n = n.child;
        }
        return n;
      case 9:
        return l = n.type, r = n.pendingProps.children, An(n, t), l = ve3(l), r = r(l), n.flags |= 1, q2(e2, n, r, t), n.child;
      case 14:
        return r = n.type, l = we3(r, n.pendingProps), l = we3(r.type, l), bu(e2, n, r, l, t);
      case 15:
        return Hs(e2, n, n.type, n.pendingProps, t);
      case 17:
        return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : we3(r, l), cr(e2, n), n.tag = 1, le2(r) ? (e2 = true, xr(n)) : e2 = false, An(n, t), ys(n, r, l), bl(n, r, l, t), ti(null, n, r, true, e2, t);
      case 19:
        return Ys(e2, n, t);
      case 22:
        return Ws(e2, n, t);
    }
    throw Error(v(156, n.tag));
  };
  function aa(e2, n) {
    return Fo(e2, n);
  }
  function gf(e2, n, t, r) {
    this.tag = e2, this.key = t, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = n, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
  }
  function me3(e2, n, t, r) {
    return new gf(e2, n, t, r);
  }
  function bi(e2) {
    return e2 = e2.prototype, !(!e2 || !e2.isReactComponent);
  }
  function wf(e2) {
    if (typeof e2 == "function")
      return bi(e2) ? 1 : 0;
    if (e2 != null) {
      if (e2 = e2.$$typeof, e2 === gi)
        return 11;
      if (e2 === wi)
        return 14;
    }
    return 2;
  }
  function nn(e2, n) {
    var t = e2.alternate;
    return t === null ? (t = me3(e2.tag, n, e2.key, e2.mode), t.elementType = e2.elementType, t.type = e2.type, t.stateNode = e2.stateNode, t.alternate = e2, e2.alternate = t) : (t.pendingProps = n, t.type = e2.type, t.flags = 0, t.subtreeFlags = 0, t.deletions = null), t.flags = e2.flags & 14680064, t.childLanes = e2.childLanes, t.lanes = e2.lanes, t.child = e2.child, t.memoizedProps = e2.memoizedProps, t.memoizedState = e2.memoizedState, t.updateQueue = e2.updateQueue, n = e2.dependencies, t.dependencies = n === null ? null : { lanes: n.lanes, firstContext: n.firstContext }, t.sibling = e2.sibling, t.index = e2.index, t.ref = e2.ref, t;
  }
  function pr(e2, n, t, r, l, i) {
    var u = 2;
    if (r = e2, typeof e2 == "function")
      bi(e2) && (u = 1);
    else if (typeof e2 == "string")
      u = 5;
    else
      e:
        switch (e2) {
          case Nn:
            return mn(t.children, l, i, n);
          case yi:
            u = 8, l |= 8;
            break;
          case Cl:
            return e2 = me3(12, t, n, l | 2), e2.elementType = Cl, e2.lanes = i, e2;
          case xl:
            return e2 = me3(13, t, n, l), e2.elementType = xl, e2.lanes = i, e2;
          case Nl:
            return e2 = me3(19, t, n, l), e2.elementType = Nl, e2.lanes = i, e2;
          case go:
            return Xr(t, l, i, n);
          default:
            if (typeof e2 == "object" && e2 !== null)
              switch (e2.$$typeof) {
                case vo:
                  u = 10;
                  break e;
                case yo:
                  u = 9;
                  break e;
                case gi:
                  u = 11;
                  break e;
                case wi:
                  u = 14;
                  break e;
                case He:
                  u = 16, r = null;
                  break e;
              }
            throw Error(v(130, e2 == null ? e2 : typeof e2, ""));
        }
    return n = me3(u, t, n, l), n.elementType = e2, n.type = r, n.lanes = i, n;
  }
  function mn(e2, n, t, r) {
    return e2 = me3(7, e2, r, n), e2.lanes = t, e2;
  }
  function Xr(e2, n, t, r) {
    return e2 = me3(22, e2, r, n), e2.elementType = go, e2.lanes = t, e2.stateNode = { isHidden: false }, e2;
  }
  function Sl(e2, n, t) {
    return e2 = me3(6, e2, null, n), e2.lanes = t, e2;
  }
  function kl(e2, n, t) {
    return n = me3(4, e2.children !== null ? e2.children : [], e2.key, n), n.lanes = t, n.stateNode = { containerInfo: e2.containerInfo, pendingChildren: null, implementation: e2.implementation }, n;
  }
  function Sf(e2, n, t, r, l) {
    this.tag = n, this.containerInfo = e2, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = ll(0), this.expirationTimes = ll(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = ll(0), this.identifierPrefix = r, this.onRecoverableError = l, this.mutableSourceEagerHydrationData = null;
  }
  function eu(e2, n, t, r, l, i, u, o, s) {
    return e2 = new Sf(e2, n, t, o, s), n === 1 ? (n = 1, i === true && (n |= 8)) : n = 0, i = me3(3, null, null, n), e2.current = i, i.stateNode = e2, i.memoizedState = { element: r, isDehydrated: t, cache: null, transitions: null, pendingSuspenseBoundaries: null }, ji(i), e2;
  }
  function kf(e2, n, t) {
    var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
    return { $$typeof: xn, key: r == null ? null : "" + r, children: e2, containerInfo: n, implementation: t };
  }
  function ca(e2) {
    if (!e2)
      return rn;
    e2 = e2._reactInternals;
    e: {
      if (kn(e2) !== e2 || e2.tag !== 1)
        throw Error(v(170));
      var n = e2;
      do {
        switch (n.tag) {
          case 3:
            n = n.stateNode.context;
            break e;
          case 1:
            if (le2(n.type)) {
              n = n.stateNode.__reactInternalMemoizedMergedChildContext;
              break e;
            }
        }
        n = n.return;
      } while (n !== null);
      throw Error(v(171));
    }
    if (e2.tag === 1) {
      var t = e2.type;
      if (le2(t))
        return as(e2, t, n);
    }
    return n;
  }
  function fa(e2, n, t, r, l, i, u, o, s) {
    return e2 = eu(t, r, true, e2, l, i, u, o, s), e2.context = ca(null), t = e2.current, r = b(), l = en(t), i = Re2(r, l), i.callback = n ?? null, qe2(t, i, l), e2.current.lanes = l, Ft(e2, l, r), ie(e2, r), e2;
  }
  function Gr(e2, n, t, r) {
    var l = n.current, i = b(), u = en(l);
    return t = ca(t), n.context === null ? n.context = t : n.pendingContext = t, n = Re2(i, u), n.payload = { element: e2 }, r = r === void 0 ? null : r, r !== null && (n.callback = r), e2 = qe2(l, n, u), e2 !== null && (Ce2(e2, l, u, i), or(e2, l, u)), u;
  }
  function jr(e2) {
    if (e2 = e2.current, !e2.child)
      return null;
    switch (e2.child.tag) {
      case 5:
        return e2.child.stateNode;
      default:
        return e2.child.stateNode;
    }
  }
  function fo(e2, n) {
    if (e2 = e2.memoizedState, e2 !== null && e2.dehydrated !== null) {
      var t = e2.retryLane;
      e2.retryLane = t !== 0 && t < n ? t : n;
    }
  }
  function nu(e2, n) {
    fo(e2, n), (e2 = e2.alternate) && fo(e2, n);
  }
  function Ef() {
    return null;
  }
  var da = typeof reportError == "function" ? reportError : function(e2) {
    console.error(e2);
  };
  function tu(e2) {
    this._internalRoot = e2;
  }
  Zr.prototype.render = tu.prototype.render = function(e2) {
    var n = this._internalRoot;
    if (n === null)
      throw Error(v(409));
    Gr(e2, n, null, null);
  };
  Zr.prototype.unmount = tu.prototype.unmount = function() {
    var e2 = this._internalRoot;
    if (e2 !== null) {
      this._internalRoot = null;
      var n = e2.containerInfo;
      wn(function() {
        Gr(null, e2, null, null);
      }), n[Ie3] = null;
    }
  };
  function Zr(e2) {
    this._internalRoot = e2;
  }
  Zr.prototype.unstable_scheduleHydration = function(e2) {
    if (e2) {
      var n = Ho();
      e2 = { blockedOn: null, target: e2, priority: n };
      for (var t = 0; t < Qe.length && n !== 0 && n < Qe[t].priority; t++)
        ;
      Qe.splice(t, 0, e2), t === 0 && Qo(e2);
    }
  };
  function ru(e2) {
    return !(!e2 || e2.nodeType !== 1 && e2.nodeType !== 9 && e2.nodeType !== 11);
  }
  function Jr(e2) {
    return !(!e2 || e2.nodeType !== 1 && e2.nodeType !== 9 && e2.nodeType !== 11 && (e2.nodeType !== 8 || e2.nodeValue !== " react-mount-point-unstable "));
  }
  function po() {
  }
  function Cf(e2, n, t, r, l) {
    if (l) {
      if (typeof r == "function") {
        var i = r;
        r = function() {
          var d = jr(u);
          i.call(d);
        };
      }
      var u = fa(n, r, e2, 0, null, false, false, "", po);
      return e2._reactRootContainer = u, e2[Ie3] = u.current, _t(e2.nodeType === 8 ? e2.parentNode : e2), wn(), u;
    }
    for (; l = e2.lastChild; )
      e2.removeChild(l);
    if (typeof r == "function") {
      var o = r;
      r = function() {
        var d = jr(s);
        o.call(d);
      };
    }
    var s = eu(e2, 0, false, null, null, false, false, "", po);
    return e2._reactRootContainer = s, e2[Ie3] = s.current, _t(e2.nodeType === 8 ? e2.parentNode : e2), wn(function() {
      Gr(n, s, t, r);
    }), s;
  }
  function qr(e2, n, t, r, l) {
    var i = t._reactRootContainer;
    if (i) {
      var u = i;
      if (typeof l == "function") {
        var o = l;
        l = function() {
          var s = jr(u);
          o.call(s);
        };
      }
      Gr(n, u, e2, l);
    } else
      u = Cf(t, n, e2, l, r);
    return jr(u);
  }
  Ao = function(e2) {
    switch (e2.tag) {
      case 3:
        var n = e2.stateNode;
        if (n.current.memoizedState.isDehydrated) {
          var t = ot(n.pendingLanes);
          t !== 0 && (Ei(n, t | 1), ie(n, U3()), (_ & 6) === 0 && (Xn = U3() + 500, on()));
        }
        break;
      case 13:
        wn(function() {
          var r = je2(e2, 1);
          if (r !== null) {
            var l = b();
            Ce2(r, e2, 1, l);
          }
        }), nu(e2, 1);
    }
  };
  Ci = function(e2) {
    if (e2.tag === 13) {
      var n = je2(e2, 134217728);
      if (n !== null) {
        var t = b();
        Ce2(n, e2, 134217728, t);
      }
      nu(e2, 134217728);
    }
  };
  Bo = function(e2) {
    if (e2.tag === 13) {
      var n = en(e2), t = je2(e2, n);
      if (t !== null) {
        var r = b();
        Ce2(t, e2, n, r);
      }
      nu(e2, n);
    }
  };
  Ho = function() {
    return P;
  };
  Wo = function(e2, n) {
    var t = P;
    try {
      return P = e2, n();
    } finally {
      P = t;
    }
  };
  Fl = function(e2, n, t) {
    switch (n) {
      case "input":
        if (Pl(e2, t), n = t.name, t.type === "radio" && n != null) {
          for (t = e2; t.parentNode; )
            t = t.parentNode;
          for (t = t.querySelectorAll("input[name=" + JSON.stringify("" + n) + '][type="radio"]'), n = 0; n < t.length; n++) {
            var r = t[n];
            if (r !== e2 && r.form === e2.form) {
              var l = Hr(r);
              if (!l)
                throw Error(v(90));
              So(r), Pl(r, l);
            }
          }
        }
        break;
      case "textarea":
        Eo(e2, t);
        break;
      case "select":
        n = t.value, n != null && In(e2, !!t.multiple, n, false);
    }
  };
  Lo = Zi;
  To = wn;
  var xf = { usingClientEntryPoint: false, Events: [jt, Ln, Hr, zo, Po, Zi] }, rt = { findFiberByHostInstance: cn, bundleType: 0, version: "18.2.0", rendererPackageName: "react-dom" }, Nf = { bundleType: rt.bundleType, version: rt.version, rendererPackageName: rt.rendererPackageName, rendererConfig: rt.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Ve2.ReactCurrentDispatcher, findHostInstanceByFiber: function(e2) {
    return e2 = Oo(e2), e2 === null ? null : e2.stateNode;
  }, findFiberByHostInstance: rt.findFiberByHostInstance || Ef, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.2.0-next-9e3b772b8-20220608" };
  if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && (lt = __REACT_DEVTOOLS_GLOBAL_HOOK__, !lt.isDisabled && lt.supportsFiber))
    try {
      Ur = lt.inject(Nf), Pe3 = lt;
    } catch {
    }
  var lt;
  fe3.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = xf;
  fe3.createPortal = function(e2, n) {
    var t = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
    if (!ru(n))
      throw Error(v(200));
    return kf(e2, n, null, t);
  };
  fe3.createRoot = function(e2, n) {
    if (!ru(e2))
      throw Error(v(299));
    var t = false, r = "", l = da;
    return n != null && (n.unstable_strictMode === true && (t = true), n.identifierPrefix !== void 0 && (r = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), n = eu(e2, 1, false, null, null, t, false, r, l), e2[Ie3] = n.current, _t(e2.nodeType === 8 ? e2.parentNode : e2), new tu(n);
  };
  fe3.findDOMNode = function(e2) {
    if (e2 == null)
      return null;
    if (e2.nodeType === 1)
      return e2;
    var n = e2._reactInternals;
    if (n === void 0)
      throw typeof e2.render == "function" ? Error(v(188)) : (e2 = Object.keys(e2).join(","), Error(v(268, e2)));
    return e2 = Oo(n), e2 = e2 === null ? null : e2.stateNode, e2;
  };
  fe3.flushSync = function(e2) {
    return wn(e2);
  };
  fe3.hydrate = function(e2, n, t) {
    if (!Jr(n))
      throw Error(v(200));
    return qr(null, e2, n, true, t);
  };
  fe3.hydrateRoot = function(e2, n, t) {
    if (!ru(e2))
      throw Error(v(405));
    var r = t != null && t.hydratedSources || null, l = false, i = "", u = da;
    if (t != null && (t.unstable_strictMode === true && (l = true), t.identifierPrefix !== void 0 && (i = t.identifierPrefix), t.onRecoverableError !== void 0 && (u = t.onRecoverableError)), n = fa(n, null, e2, 1, t ?? null, l, false, i, u), e2[Ie3] = n.current, _t(e2), r)
      for (e2 = 0; e2 < r.length; e2++)
        t = r[e2], l = t._getVersion, l = l(t._source), n.mutableSourceEagerHydrationData == null ? n.mutableSourceEagerHydrationData = [t, l] : n.mutableSourceEagerHydrationData.push(t, l);
    return new Zr(n);
  };
  fe3.render = function(e2, n, t) {
    if (!Jr(n))
      throw Error(v(200));
    return qr(null, e2, n, false, t);
  };
  fe3.unmountComponentAtNode = function(e2) {
    if (!Jr(e2))
      throw Error(v(40));
    return e2._reactRootContainer ? (wn(function() {
      qr(null, null, e2, false, function() {
        e2._reactRootContainer = null, e2[Ie3] = null;
      });
    }), true) : false;
  };
  fe3.unstable_batchedUpdates = Zi;
  fe3.unstable_renderSubtreeIntoContainer = function(e2, n, t, r) {
    if (!Jr(t))
      throw Error(v(200));
    if (e2 == null || e2._reactInternals === void 0)
      throw Error(v(38));
    return qr(e2, n, t, false, r);
  };
  fe3.version = "18.2.0-next-9e3b772b8-20220608";
});
var va = uu((Pf, ha) => {
  "use strict";
  function ma() {
    if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
      try {
        __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(ma);
      } catch (e2) {
        console.error(e2);
      }
  }
  ma(), ha.exports = pa();
});
var br = xa(va());
var Bf = br.default ?? br;

// bigframes/display/src/index.js
var e = Be.createElement;
function TableWidget({ model }) {
  const [page, setPage] = qe(model.get("page"));
  const [pageSize, setPageSize] = qe(model.get("page_size"));
  const [maxColumns, setMaxColumns] = qe(model.get("max_columns"));
  const [tableHtml, setTableHtml] = qe(model.get("table_html"));
  const [rowCount, setRowCount] = qe(model.get("row_count"));
  const [errorMessage, setErrorMessage] = qe(model.get("error_message"));
  const [sortContext, setSortContext] = qe(model.get("sort_context") || []);
  const [orderableColumns, setOrderableColumns] = qe(model.get("orderable_columns") || []);
  const [deferredMode, setDeferredMode] = qe(model.get("deferred_mode"));
  const [executionState, setExecutionState] = qe(model.get("execution_state") || "idle");
  const tableContainerRef = Ue(null);
  Pe(() => {
    const handleChange = () => {
      setPage(model.get("page"));
      setPageSize(model.get("page_size"));
      setMaxColumns(model.get("max_columns"));
      setTableHtml(model.get("table_html"));
      setRowCount(model.get("row_count"));
      setErrorMessage(model.get("error_message"));
      setSortContext(model.get("sort_context") || []);
      setOrderableColumns(model.get("orderable_columns") || []);
      setDeferredMode(model.get("deferred_mode"));
      setExecutionState(model.get("execution_state") || "idle");
    };
    model.on("change", handleChange);
    return () => model.off("change", handleChange);
  }, [model]);
  Pe(() => {
    const tableContainer = tableContainerRef.current;
    if (!tableContainer)
      return;
    const headers = tableContainer.querySelectorAll("th");
    headers.forEach((header) => {
      const headerDiv = header.querySelector("div");
      if (!headerDiv)
        return;
      const columnName = headerDiv.textContent.trim();
      if (columnName && orderableColumns.includes(columnName)) {
        header.style.cursor = "pointer";
        const indicatorSpan = document.createElement("span");
        indicatorSpan.classList.add("sort-indicator");
        indicatorSpan.style.paddingLeft = "5px";
        const sortIndex = sortContext.findIndex((item) => item.column === columnName);
        let indicator = "\u25CF";
        if (sortIndex !== -1) {
          const isAscending = sortContext[sortIndex].ascending;
          indicator = isAscending ? "\u25B2" : "\u25BC";
          indicatorSpan.style.visibility = "visible";
        } else {
          indicatorSpan.style.visibility = "hidden";
        }
        indicatorSpan.textContent = indicator;
        const existingIndicator = headerDiv.querySelector(".sort-indicator");
        if (existingIndicator) {
          headerDiv.removeChild(existingIndicator);
        }
        headerDiv.appendChild(indicatorSpan);
        header.addEventListener("mouseover", () => {
          if (sortContext.findIndex((item) => item.column === columnName) === -1) {
            indicatorSpan.style.visibility = "visible";
          }
        });
        header.addEventListener("mouseout", () => {
          if (sortContext.findIndex((item) => item.column === columnName) === -1) {
            indicatorSpan.style.visibility = "hidden";
          }
        });
        header.addEventListener("click", (event) => {
          const currentSortIndex = sortContext.findIndex((item) => item.column === columnName);
          let newContext = [...sortContext];
          if (event.shiftKey) {
            if (currentSortIndex !== -1) {
              if (newContext[currentSortIndex].ascending) {
                newContext[currentSortIndex] = { ...newContext[currentSortIndex], ascending: false };
              } else {
                newContext.splice(currentSortIndex, 1);
              }
            } else {
              newContext.push({ column: columnName, ascending: true });
            }
          } else {
            if (currentSortIndex !== -1 && newContext.length === 1) {
              if (newContext[currentSortIndex].ascending) {
                newContext[currentSortIndex] = { ...newContext[currentSortIndex], ascending: false };
              } else {
                newContext = [];
              }
            } else {
              newContext = [{ column: columnName, ascending: true }];
            }
          }
          model.set("sort_context", newContext);
          model.save_changes();
        });
      }
    });
  }, [tableHtml, sortContext, orderableColumns, model]);
  const handlePageChange = (direction) => {
    model.set("page", page + direction);
    model.save_changes();
  };
  const handlePageSizeChange = (e2) => {
    const newSize = Number(e2.target.value);
    model.set("page_size", newSize);
    model.set("page", 0);
    model.save_changes();
  };
  const handleMaxColumnsChange = (e2) => {
    const newVal = Number(e2.target.value);
    model.set("max_columns", newVal);
    model.save_changes();
  };
  const pageSizes = [10, 25, 50, 100];
  const maxColumnOptions = [5, 10, 15, 20, 0];
  const totalPages = rowCount ? Math.ceil(rowCount / pageSize) : 1;
  if (deferredMode && executionState === "idle") {
    return e("div", { className: "bigframes-widget" }, e("div", { className: "deferred-container", style: { padding: "20px", textAlign: "center" } }, e("button", {
      className: "execute-button",
      onClick: () => {
        model.set("execution_state", "executing");
        model.save_changes();
      }
    }, "Execute Query")));
  }
  if (deferredMode && executionState === "executing") {
    return e("div", { className: "bigframes-widget" }, e("div", { className: "loading-container", style: { padding: "20px", textAlign: "center" } }, "Executing query..."));
  }
  return e("div", { className: "bigframes-widget" }, errorMessage && e("div", { className: "bigframes-error-message" }, errorMessage), e("div", {
    className: "table-container",
    ref: tableContainerRef,
    dangerouslySetInnerHTML: { __html: tableHtml }
  }), e("footer", { className: "footer" }, e("span", { className: "row-count" }, rowCount === null ? "Total rows unknown" : `${rowCount.toLocaleString()} total rows`), e("div", { className: "pagination" }, e("button", { onClick: () => handlePageChange(-1), disabled: page === 0 }, "<"), e("span", { className: "page-indicator" }, rowCount === null ? `Page ${(page + 1).toLocaleString()} of many` : `Page ${(page + 1).toLocaleString()} of ${totalPages.toLocaleString()}`), e("button", { onClick: () => handlePageChange(1), disabled: rowCount !== null && page >= totalPages - 1 }, ">")), e("div", { className: "settings" }, e("div", { className: "max-columns" }, e("label", null, "Max columns:"), e("select", { value: maxColumns || 0, onChange: handleMaxColumnsChange }, maxColumnOptions.map((cols) => e("option", { key: cols, value: cols }, cols === 0 ? "All" : cols)))), e("div", { className: "page-size" }, e("label", null, "Page size:"), e("select", { value: pageSize, onChange: handlePageSizeChange }, pageSizes.map((size) => e("option", { key: size, value: size }, size)))))));
}
var src_default = {
  render({ model, el }) {
    const root = Bf.createRoot(el);
    root.render(e(TableWidget, { model }));
  }
};
export {
  src_default as default
};
/*! Bundled license information:

react-dom/cjs/react-dom.production.min.js:
  (**
   * @license React
   * react-dom.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)
*/
/*! Bundled license information:

react/cjs/react.production.min.js:
  (**
   * @license React
   * react.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)
*/
/*! Bundled license information:

scheduler/cjs/scheduler.production.min.js:
  (**
   * @license React
   * scheduler.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)
*/
