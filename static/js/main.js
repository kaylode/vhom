// Global variables

const dataUrl = 'http://127.0.0.1:5000/data/tp';  // Data request URL
let clicked_object = null;                        // clicked marker
var map_id = null;                                // Leaflet Map ID


function changeMarkerIconColor(object, color) {
    /*
        Change marker icon color
    */
    var icon = L.AwesomeMarkers.icon({
        "extraClasses": "fa-rotate-0", 
        "icon": "info-sign", 
        "iconColor": "white", 
        "markerColor": color, 
        "prefix": "glyphicon"}
    );
    object.setIcon(icon);
    return object;
}

function onClick(e) {
    /*
        On click event of leaflet markers (call by server)
    */

    // Find div contains map, margin left
    document.getElementById(map_id).style.marginLeft = "25%";

    // Show Panel on the left, to add VEGA plot
    $("#float_panel").show();
    $("#float_panel").css("width", "25%");
    $("#float_panel").css("height", "100%");

    // Add VEGA plot
    response = httpGet(dataUrl);
    visualization('#vis', JSON.parse(response));

    // Turn off current clicked marker, color new marker
    if (clicked_object) {
        changeMarkerIconColor(clicked_object, 'blue');
    }
    clicked_object = changeMarkerIconColor(this, 'green');
}

function visualization(div, json_data){
    /*
        Embed VEGA plot to div
    */
    vegaEmbed(div, json_data);
}

window.onload = function(){
    /*
        On load window functions
    */

    // Find map id
    map_id = document.getElementsByClassName('folium-map')[0].id;

    // Set on click event for close button
    document.getElementById('close').onclick = function(){
        document.getElementById(map_id).style.marginLeft = "0%";
    };
};

function httpGet(url){
    /*
        Send GET request to url
    */
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

