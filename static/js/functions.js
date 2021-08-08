function onClick(e) {
  $("#float_panel").show();
  document.getElementById("map_65c9db0f7f82458991064fe3ca38d7f5").style.marginLeft = "25%";
  $("#float_panel").css("width", "25%");
  $("#float_panel").css("height", "100%");
  visualization()
}

function visualization(){
  const spec = "static/data/bar.json";
  vegaEmbed('#vis', spec);
}

window.onload = function(){
  document.getElementById('close').onclick = function(){
    document.getElementById("map_65c9db0f7f82458991064fe3ca38d7f5").style.marginLeft = "0%";
  };
};