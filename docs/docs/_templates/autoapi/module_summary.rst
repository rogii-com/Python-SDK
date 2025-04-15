{% macro _render_item_name(obj, sig=False) -%}
`{{ obj.name }} <#{{ obj.id|replace('_', '\_') }}>`_
     {%- if sig -%}
       \ (
       {%- for arg in obj.obj.args -%}
          {%- if arg[0] %}{{ arg[0]|replace('*', '\*') }}{% endif -%}{{  arg[1] -}}
          {%- if not loop.last  %}, {% endif -%}
       {%- endfor -%}
       ){%- endif -%}
{%- endmacro %}

{% macro _item(obj, sig=False, label='') %}
   * - {% if label %}:summarylabel-{{ obj.type }}:`{{ label }}` {% endif %}{{ _render_item_name(obj, sig) }}
     - {% if obj.summary %}{{ obj.summary }}{% else %}\-{% endif +%}
{% endmacro %}

{% macro _class(cls) %}
.. list-table:: :class:`{{ cls.name }}`
   :header-rows: 0
   :widths: 40 60
   :class: summarytable

{% for obj in cls.children | rejectattr("skip") if not obj.name.startswith('_') -%}
    {%- set sig = (obj.type in ['method', 'function'] and not 'property' in obj.properties) -%}

    {%- if obj.type in ['class'] -%}
      {%- set label = 'class' -%}
    {%- elif obj.type in ['method', 'function'] -%}
      {%- set label = 'method' -%}
    {%- elif obj.type in ['property'] -%}
      {%- set label = 'property' -%}
    {%- else -%}
      {%- set label = '' -%}
    {%- endif -%}

    {{- _item(obj, sig=sig, label=label) -}}
  {%- endfor -%}
{% endmacro %}

{% macro auto_summary(objs) -%}
  {% for obj in objs -%}
    {%- if obj.type in ['class'] -%}
      {{ _class(obj) }}
    {%- endif -%}
  {%- endfor -%}
{% endmacro %}