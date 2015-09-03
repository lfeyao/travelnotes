var geocoder;
var map;
var location;

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {vars[key] = value;});
    return vars;
}

function initialize() {
    var mapCanvas = document.getElementById('detailmap');               
    geocoder = new google.maps.Geocoder();
    var address = "{{page_name_url}}";
    
    //location = getUrlVars()["location"];
    //alert(location);

    var latlng = new google.maps.LatLng(-34.397, 150.644);

    geocoder.geocode({ 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var mapOptions = {
                //center: latlng,
                center: results[0].geometry.location,
                zoom: 5,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            }

            map = new google.maps.Map(mapCanvas, mapOptions);
            //var marker = new google.maps.Marker({map: map, position: results[0].geometry.location});
            //map.setCenter(results[0].geometry.location);
        }
        else{
            var mapOptions = {
                center: latlng,
                zoom: 5,
                mapTypeId: google.maps.MapTypeId.ROADMAP
                //var marker = new google.maps.Marker({map: map, position: results[0].geometry.location});
            }
            map = new google.maps.Map(mapCanvas, mapOptions);    
        }
    });

    //geocodeAddress("Germany");
}

function geocodeAddress(address, place_name) {
    if (address){ 
        geocoder.geocode({'address': address}, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                map.setZoom(15);
                var marker = new google.maps.Marker({map: map, position: results[0].geometry.location});
            } 
            else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    }
    else
        geocoder.geocode({'place_name': place_name}, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                map.setZoom(15);
                var marker = new google.maps.Marker({map: map, position: results[0].geometry.location});
            } 
            else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
}

google.maps.event.addDomListener(window, 'load', initialize);