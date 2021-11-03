// Global variables

const dataUrl = new URL('http://192.168.100.9:5000/data');  // Data request URL
let clicked_object = null;                        // clicked marker
var map_id = null;                                // Leaflet Map ID
var camera_id = null;

function setDateBox() {
    const d = new Date();
    let daytofweek = d.getDay();

    switch (daytofweek){
        case 0: daytofweek_str = "Thứ hai"; break;
        case 1: daytofweek_str = "Thứ ba"; break;
        case 2: daytofweek_str = "Thứ tư"; break;
        case 3: daytofweek_str = "Thứ năm"; break;
        case 4: daytofweek_str = "Thứ sáu"; break;
        case 5: daytofweek_str = "Thứ bảy"; break;
        case 6: daytofweek_str = "Chủ nhật"; break;
    }

    let day = d.getDate();
    let month = d.getMonth();
    let year = d.getFullYear();
    let date = `${daytofweek_str}, ngày <strong>${day}</strong> tháng <strong>${month}</strong> năm <strong>${year}</strong>`;

    var date_element = document.getElementById("date");
    date_element.innerHTML=date;

    var s = d.getSeconds();
    var m = d.getMinutes();
    var h = d.getHours();

    var time_element = document.getElementById("time");

    time_element.innerHTML = 
        ("0" + h).substr(-2) + ":" + ("0" + m).substr(-2) + ":" + ("0" + s).substr(-2);
}

function changeMarkerIconColor(object, color) {
    /*
        Change marker icon color
    */
    var icon = L.AwesomeMarkers.icon({
        "extraClasses": "fa-rotate-0", 
        "icon": "tint", 
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
    var btn = document.getElementById("close_arrow");
    if(element.classList.contains("translate-x-full")) {
        element.classList.remove("translate-x-full");
        element.classList.add("translate-x-0");
        btn.src="https://cdn-icons-png.flaticon.com/512/50/50621.png";
    }

    document.getElementById("city-info-box").style.display = 'block';


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
    var btn = document.getElementById("close_arrow");
    if(element.classList.contains("translate-x-0")) {
        element.classList.remove("translate-x-0");
        element.classList.add("translate-x-full");
        btn.src="https://cdn-icons-png.flaticon.com/512/56/56760.png";
    }
    else {
        element.classList.remove("translate-x-full");
        element.classList.add("translate-x-0");
        btn.src="https://cdn-icons-png.flaticon.com/512/50/50621.png";
    }

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

function onMapClick() {
    var element = document.getElementById("sliding_anim");
    if(element.classList.contains("translate-x-full")){
        element.classList.remove("translate-x-full");
        element.classList.add("translate-x-0");
        btn.src="https://cdn-icons-png.flaticon.com/512/50/50621.png";
    }

    document.getElementById("city-info-box").style.display = 'none';
}

window.onload = function(){
    /*
        On load window functions
    */

    // Find map id
    map = document.getElementsByClassName('folium-map')[0]
    map_id = map.id;

    // Set on click event for close button
    document.getElementById('close').onclick = onCloseClick;

    setInterval(setDateBox, 1000);
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

