const dataUrl = 'http://127.0.0.1:5000/data/tp';

let clicked_object = null;


function changeIconColor(object, color) {
  var icon = L.AwesomeMarkers.icon(
    {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": color, "prefix": "glyphicon"}
  );
  object.setIcon(icon);
  return object;
}

function onClick(e) {
  var map_id = document.getElementsByClassName('folium-map')[0].id;
  $("#float_panel").show();
  document.getElementById(map_id).style.marginLeft = "25%";
  $("#float_panel").css("width", "25%");
  $("#float_panel").css("height", "100%");
  response = httpGet(dataUrl);
  console.log(response);
  visualization();
  if (clicked_object) {
    changeIconColor(clicked_object, 'blue');
  }
  clicked_object = changeIconColor(this, 'green');
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

function httpGet(url)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

