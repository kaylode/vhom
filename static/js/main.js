// Global variables

const dataUrl = new URL('http://127.0.0.1:5000/data');  // Data request URL
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
    $("#float_panel").show();
    $("#float_panel2").show();

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
    $("#float_panel").hide();
    $("#float_panel2").hide();

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
        getVEGAPlot(dataUrl, '#vis', 'hourly');
        setContentText('dropdown', '▼ Biểu đồ theo giờ');
    }

    document.getElementById('type2').onclick = function(){
        getVEGAPlot(dataUrl, '#vis', 'daily');
        setContentText('dropdown', '▼ Biểu đồ theo ngày');
    }

    $('#float_panel2').css({
        "float":"right",
        "top": "60%",
        "left": "70%",
        "color": "black",
        "background-color": "white",
        "width":"25%",
        "text-align": "justify"
    });

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
    
    // Initialize floating div
    initFloatingDiv();
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

