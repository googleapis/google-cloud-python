{{ fullname | escape | underline}}

..
   Originally at
   https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/autosummary/templates/autosummary/module.rst
   with modifications to support recursive generation from
   https://github.com/sphinx-doc/sphinx/issues/7912

.. automodule:: {{ fullname }}
   :no-members:

   {% block functions %}
   {%- if functions %}
   .. rubric:: {{ _('Functions') }}

   .. autosummary::
      :toctree:
   {% for item in functions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {%- endblock %}

   {%- block classes %}
   {%- if classes %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::
      :toctree:
   {% for item in classes %}{% if item not in attributes %}
      {{ item }}
   {% endif %}{%- endfor %}
   {% endif %}
   {%- endblock %}

   {%- block exceptions %}
   {%- if exceptions %}
   .. rubric:: {{ _('Exceptions') }}

   .. autosummary::
      :toctree:
   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {%- endblock %}

{%- block attributes %}
{%- if attributes %}
.. rubric:: {{ _('Module Attributes') }}

{% for item in attributes %}
.. autoattribute:: {{ fullname }}.{{ item }}
   :no-index:
{% endfor %}
{% endif %}
{%- endblock %}
