function onClick(e) {
  var map_id = document.getElementsByClassName('folium-map')[0].id;
  $("#float_panel").show();
  document.getElementById(map_id).style.marginLeft = "25%";
  $("#float_panel").css("width", "25%");
  $("#float_panel").css("height", "100%");
  visualization()
}

function visualization(){
  const spec = "static/data/bar.json";
  vegaEmbed('#vis', spec);
}

window.onload = function(){
  var map_id = document.getElementsByClassName('folium-map')[0].id;
  document.getElementById('close').onclick = function(){
    document.getElementById(map_id).style.marginLeft = "0%";
  };
};