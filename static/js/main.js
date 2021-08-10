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

function onMarkerClick(e) {
    /*
        On click event of leaflet markers (call by server)
    */

    // Show Panel on the right, to add VEGA plot
    $("#float_panel").show();

    // Add VEGA plot
    getVEGAPlot(dataUrl, '#vis');

    // Turn off current clicked marker, color new marker
    if (clicked_object) {
        changeMarkerIconColor(clicked_object, 'blue');
    }
    clicked_object = changeMarkerIconColor(this, 'green');
}

function onCloseClick(){
    /*
        On click event for close button
    */

    // Hide VEGA plot
    $("#float_panel").hide();

    if (clicked_object) {
        changeMarkerIconColor(clicked_object, 'blue');
    }
    clicked_object = null;
}

function getVEGAPlot(url, id) {
    /*
        Send get request and plot VEGA
    */
    response = httpGet(url);
    visualization(id, JSON.parse(response));
}

function initFloatingDiv() {
    /*
        Set custom DIV and dropdowns
    */
    $('#float_panel').css({
        "float":"right",
        "top": "10%",
        "left": "70%",
        "color": "red",
        "background-color": "white",
        "width":"25%",
    });

    document.getElementById('type1').onclick = function(){
        getVEGAPlot(dataUrl, '#vis');
    }

    document.getElementById('type2').onclick = function(){
        getVEGAPlot(dataUrl, '#vis');
    }
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
    document.getElementById('close').onclick = onCloseClick;
    
    // Initialize floating div
    initFloatingDiv();
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

