{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

{% block methods %}
{% if methods %}
.. rubric:: Methods

.. autosummary::
{% for item in methods %}
   {% if item != '__init__' %}
   ~{{ name }}.{{ item }}
   {% endif %}
{%- endfor %}
{% endif %}
{% endblock %}

{% block attributes %}
{% if attributes %}
.. rubric:: Attributes

.. autosummary::
{% for item in attributes %}
   ~{{ name }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

.. raw:: html

    <p>
    <hr>
    <p>

.. autoclass:: {{ objname }}
   :members:
