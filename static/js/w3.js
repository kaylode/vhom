function onClick(e) {
  $("#float_panel").show();
  document.getElementById("map_ae2b4fd64e2a41e6a0f28c228b3ad9ed").style.marginLeft = "25%";
  $("#float_panel").css("width", "25%");
  $("#float_panel").css("height", "100%");
  visualization()
}

function visualization(){
  var yourVlSpec = {
    $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
    description: 'A simple bar chart with embedded data.',
    width: 300,
    data: {
      values: [
        {a: 'A', b: 28},
        {a: 'B', b: 55},
        {a: 'C', b: 43},
        {a: 'D', b: 91},
        {a: 'E', b: 81},
        {a: 'F', b: 53},
        {a: 'G', b: 19},
        {a: 'H', b: 87},
        {a: 'I', b: 52}
      ]
    },
    mark: 'bar',
    encoding: {
      x: {field: 'a', type: 'ordinal'},
      y: {field: 'b', type: 'quantitative'}
    }
  };
  vegaEmbed('#vis', yourVlSpec);
}

window.onload = function(){
  document.getElementById('close').onclick = function(){
    document.getElementById("map_ae2b4fd64e2a41e6a0f28c228b3ad9ed").style.marginLeft = "0%";
  };
};