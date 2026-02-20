{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

{% set is_pandas = module.startswith("bigframes.pandas") or module.startswith("bigframes.geopandas") %}
{% set skip_inherited = is_pandas and not module.startswith("bigframes.pandas.typing.api") %}

{% if is_pandas %}
.. autoclass:: {{ objname }}
   :no-members:

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
      :toctree:
   {% for item in attributes %}
      {%- if not skip_inherited or not item in inherited_members%}
      ~{{ name }}.{{ item }}
      {%- endif %}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block methods %}
   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
      :toctree:

   {% for item in methods %}
      {%- if not skip_inherited or not item in inherited_members%}
      ~{{ name }}.{{ item }}
      {%- endif %}
   {%- endfor %}
   {% endif %}
   {% endblock %}
{% else %}
.. autoclass:: {{ objname }}
{% endif %}
