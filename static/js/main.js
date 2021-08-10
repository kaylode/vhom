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

String.format = function() {
    var s = arguments[0];
    for (var i = 0; i < arguments.length - 1; i += 1) {
        var reg = new RegExp('\\{' + i + '\\}', 'gm');
        s = s.replace(reg, arguments[i + 1]);
    }
    return s;
};

function onMarkerClick(e) {
    /*
        On click event of leaflet markers (call by server)
    */

    // Show Panel on the right, to add VEGA plot
    $("#float_panel").show();
    $("#float_panel2").show();

    // Add VEGA plot
    getVEGAPlot(dataUrl, '#vis');

    // Add city info
    var cordinate = this.getLatLng();
    let lat =  String(cordinate.lat);
    let lng =  String(cordinate.lng);
    var content = String.format('&emsp;<strong>Vĩ độ</strong>: {0} <br> &emsp;<strong>Kinh độ</strong>: {1}', lat, lng);
    
    setContentText('city-info', content);

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
    $("#float_panel2").hide();

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
        setContentText('dropdown', '▼ Biểu đồ 1');
    }

    document.getElementById('type2').onclick = function(){
        getVEGAPlot(dataUrl, '#vis');
        setContentText('dropdown', '▼ Biểu đồ 2');
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
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

