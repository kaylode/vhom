// Global variables

const dataUrl = new URL('http://192.168.100.9:5000/data');  // Data request URL
let clicked_object = null;                        // clicked marker
var map_id = null;                                // Leaflet Map ID
var camera_id = null;


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

function getContentFromDict(dict) {
    /*
        Get data sent with on click marker
    */
    var content = "";
    for (const [key, value] of Object.entries(dict)) {
        content = content.concat(`&emsp; <strong>${key}</strong>: ${value}<br>`);
    }
    return content;
}

function onMarkerClick(e, dict) {
    /*
        On click event of leaflet markers (call by server)
    */
    // Show Panel on the right, to add VEGA plot
    var element = document.getElementById("sliding_anim");
    element.classList.remove("translate-x-full");
    element.classList.add("translate-x-0");


    // Set camera id
    camera_id = dict['Camera id'];

    // Add VEGA plot
    getVEGAPlot(dataUrl, '#vis', 'hourly');

    // Add city info
    content = getContentFromDict(dict);
    setContentText('city-info', content);

    // Turn off current clicked marker, color new marker
    if (clicked_object) {
        changeMarkerIconColor(clicked_object, 'blue');
    }
    clicked_object = changeMarkerIconColor(e.target, 'green');
}

function onCloseClick(){
    /*
        On click event for close button
    */

    // Hide VEGA plot
    // $("#float_panel").hide();
    var element = document.getElementById("sliding_anim");
    element.classList.remove("translate-x-0");
    element.classList.add("translate-x-full");

    if (clicked_object) {
        changeMarkerIconColor(clicked_object, 'blue');
    }
    clicked_object = null;
}

function getVEGAPlot(url, id, type) {
    /*
        Send get request and plot VEGA
    */
    url.searchParams.set('type', type);
    url.searchParams.set('cameraId', camera_id);

    response = httpGet(url);
    visualization(id, JSON.parse(response));
}

function setContentText(id, text) {
    document.getElementById(id).innerHTML = text;
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
    
};

function httpGet(url){
    /*
        Send GET request to url
    */

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false ); // false for synchronous request
    xmlHttp.send();
    return xmlHttp.responseText;
}

