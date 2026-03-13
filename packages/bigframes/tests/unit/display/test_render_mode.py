# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest.mock as mock

import bigframes.display.html as bf_html
import bigframes.pandas as bpd


def test_render_mode_options():
    assert bpd.options.display.render_mode == "html"

    with bpd.option_context("display.render_mode", "plaintext"):
        assert bpd.options.display.render_mode == "plaintext"

    with bpd.option_context("display.render_mode", "html"):
        assert bpd.options.display.render_mode == "html"

    with bpd.option_context("display.render_mode", "anywidget"):
        assert bpd.options.display.render_mode == "anywidget"


def test_repr_mimebundle_selection_logic():
    mock_obj = mock.Mock()

    # Mocking dependencies
    with mock.patch(
        "bigframes.display.html.repr_mimebundle_head"
    ) as mock_head, mock.patch(
        "bigframes.display.html.get_anywidget_bundle"
    ) as mock_anywidget, mock.patch(
        "bigframes.display.html.repr_mimebundle_deferred"
    ) as mock_deferred:
        mock_head.side_effect = lambda obj: {"text/plain": "plain", "text/html": "html"}
        mock_anywidget.return_value = (
            {
                "application/vnd.jupyter.widget-view+json": {},
                "text/plain": "plain",
                "text/html": "html",
            },
            {},
        )
        mock_deferred.return_value = {"text/plain": "deferred"}

        # Test deferred repr_mode
        with bpd.option_context("display.repr_mode", "deferred"):
            bundle = bf_html.repr_mimebundle(mock_obj)
            assert bundle == {"text/plain": "deferred"}
            mock_deferred.assert_called_once()
            mock_head.assert_not_called()

        mock_deferred.reset_mock()

        # Test plaintext render_mode
        with bpd.option_context("display.render_mode", "plaintext"):
            bundle = bf_html.repr_mimebundle(mock_obj)
            assert "text/plain" in bundle
            assert "text/html" not in bundle
            mock_head.assert_called_once()

        mock_head.reset_mock()

        # Test html render_mode
        with bpd.option_context("display.render_mode", "html"):
            bundle = bf_html.repr_mimebundle(mock_obj)
            assert "text/plain" in bundle
            assert "text/html" in bundle
            mock_head.assert_called_once()

        mock_head.reset_mock()

        # Test anywidget render_mode
        with bpd.option_context("display.render_mode", "anywidget"):
            bundle = bf_html.repr_mimebundle(mock_obj)
            assert "application/vnd.jupyter.widget-view+json" in bundle[0]
            mock_anywidget.assert_called_once()
            mock_head.assert_not_called()

        mock_anywidget.reset_mock()

        # Test anywidget repr_mode (backward compatibility)
        with bpd.option_context("display.repr_mode", "anywidget"):
            bundle = bf_html.repr_mimebundle(mock_obj)
            assert "application/vnd.jupyter.widget-view+json" in bundle[0]
            mock_anywidget.assert_called_once()
            mock_head.assert_not_called()

        mock_anywidget.reset_mock()

        # Test default render_mode (should be "html")
        bundle = bf_html.repr_mimebundle(mock_obj)
        assert "text/plain" in bundle
        assert "text/html" in bundle
        mock_head.assert_called_once()
        mock_anywidget.assert_not_called()
