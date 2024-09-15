<script>
  export let legend_data, legend_color_function;
</script>

{#each legend_data as d, i}
  <rect
    x="25"
    y={i * 30 + 10}
    width="20"
    height="20"
    fill={legend_color_function(d)}
  />
  <text class="text fill-gray-200 text-base" x="60" y={25 + i * 30}
    >{d[0] + d.slice(1).toLowerCase()}
  </text>
{/each}
