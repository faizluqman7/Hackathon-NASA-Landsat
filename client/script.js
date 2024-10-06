document.getElementById("lat").innerHTML = localStorage.getItem("latstore");
document.getElementById("lng").innerHTML = localStorage.getItem("lngstore");

const retroStyle = [
    {
        "elementType": "geometry",
        "stylers": [
            { "color": "#ebe3cd" }
        ]
    },
    {
        "elementType": "labels.text.fill",
        "stylers": [
            { "color": "#523735" }
        ]
    },
    {
        "elementType": "labels.text.stroke",
        "stylers": [
            { "color": "#f5f1e6" }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry.stroke",
        "stylers": [
            { "color": "#c9b2a6" }
        ]
    },
    {
        "featureType": "administrative.land_parcel",
        "elementType": "geometry.stroke",
        "stylers": [
            { "color": "#dcd2be" }
        ]
    },
    {
        "featureType": "administrative.land_parcel",
        "elementType": "labels.text.fill",
        "stylers": [
            { "color": "#ae9e90" }
        ]
    },
    {
        "featureType": "landscape.natural",
        "elementType": "geometry",
        "stylers": [
            { "color": "#dfd2ae" }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [
            { "color": "#dfd2ae" }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "labels.text.fill",
        "stylers": [
            { "color": "#93817c" }
        ]
    },
    {
        "featureType": "poi.park",
        "elementType": "geometry.fill",
        "stylers": [
            { "color": "#a5b076" }
        ]
    },
    {
        "featureType": "poi.park",
        "elementType": "labels.text.fill",
        "stylers": [
            { "color": "#447530" }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry",
        "stylers": [
            { "color": "#f5f1e6" }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry",
        "stylers": [
            { "color": "#fdfcf8" }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry",
        "stylers": [
            { "color": "#f8c967" }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [
            { "color": "#e9bc62" }
        ]
    },
    {
        "featureType": "road.highway.controlled_access",
        "elementType": "geometry",
        "stylers": [
            { "color": "#e98d58" }
        ]
    },
    {
        "featureType": "road.highway.controlled_access",
        "elementType": "geometry.stroke",
        "stylers": [
            { "color": "#db8555" }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "labels.text.fill",
        "stylers": [
            { "color": "#806b63" }
        ]
    },
    {
        "featureType": "transit.line",
        "elementType": "geometry",
        "stylers": [
            { "color": "#dfd2ae" }
        ]
    },
    {
        "featureType": "transit.line",
        "elementType": "labels.text.fill",
        "stylers": [
            { "color": "#8f7d77" }
        ]
    },
    {
        "featureType": "transit.line",
        "elementType": "labels.text.stroke",
        "stylers": [
            { "color": "#ebe3cd" }
        ]
    },
    {
        "featureType": "transit.station",
        "elementType": "geometry",
        "stylers": [
            { "color": "#dfd2ae" }
        ]
    },
    {
        "featureType": "water",
        "elementType": "geometry.fill",
        "stylers": [
            { "color": "#b9d3c2" }
        ]
    },
    {
        "featureType": "water",
        "elementType": "labels.text.fill",
        "stylers": [
            { "color": "#92998d" }
        ]
    }
];

let map, marker, searchBox;

function initMap() {
    // Get user's current location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            // Initialize the map centered on user's current location with style
            map = new google.maps.Map(document.getElementById("map"), {
                zoom: 14,
                center: userLocation,
                styles: retroStyle // Apply the provided style
            });

            // Marker for selected location
            marker = new google.maps.Marker({
                position: userLocation,
                map: map,
                draggable: true
            });

            // Initialize the search box
            const input = document.getElementById("search-box");
            const autocomplete = new google.maps.places.Autocomplete(input);
            autocomplete.bindTo("bounds", map);

            // Capture the place when a user selects a location from the autocomplete dropdown
            autocomplete.addListener("place_changed", function() {
                const place = autocomplete.getPlace();
                if (!place.geometry) {
                    console.error("No details available for the selected place.");
                    return;
                }

                // Center the map on the searched location
                map.setCenter(place.geometry.location);
                map.setZoom(14);

                // Move the marker to the selected place
                marker.setPosition(place.geometry.location);
                updateCoordinates(place.geometry.location);
            });

            // Event listener to capture clicks on the map
            map.addListener("click", function(event) {
                const clickedLocation = event.latLng;
                marker.setPosition(clickedLocation);
                updateCoordinates(clickedLocation);
            });

            // Update coordinates when marker is dragged
            marker.addListener('dragend', function(event) {
                updateCoordinates(event.latLng);
            });

            // Set initial coordinates
            updateCoordinates(userLocation);

        }, function() {
            handleLocationError(true, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, map.getCenter());
    }
}

// Function to update coordinates display
function updateCoordinates(location) {
    const lat = typeof location.lat === "function" ? location.lat() : location.lat;
    const lng = typeof location.lng === "function" ? location.lng() : location.lng;

    document.getElementById('lat').innerHTML = 'Latitude: ' + lat;
    document.getElementById('lng').innerHTML = 'Longitude: ' + lng;

    localStorage.setItem("latstore" , lat);
    localStorage.setItem("lngstore" , lng);

    // Test
    sendEmail(lat, lng);
}

// Error handling for geolocation
function handleLocationError(browserHasGeolocation, pos) {
    alert(browserHasGeolocation
        ? "Error: The Geolocation service failed."
        : "Error: Your browser doesn't support geolocation.");
}

//API KEY Google Maps API= AIzaSyBgKFgyqXT86wQx7avSvCg5RkME9zqrwQc
//this is the updating coordinate for the display in below the map
	function updateCoordinates(location) {

		const lat = typeof location.lat === "function" ? location.lat() : location.lat;
     	const lng = typeof location.lng === "function" ? location.lng() : location.lng;

		document.getElementById('lat').innerHTML = 'Latitude: ' + lat;
		document.getElementById('lng').innerHTML = 'Longitude: ' + lng;

        localStorage.setItem("latstore" , lat);
        localStorage.setItem("lngstore", lng);
	}

	function handleLocationError(browserHasGeolocation, pos) {
		alert(browserHasGeolocation
			? "Error: The Geolocation service failed."
			: "Error: Your browser doesn't support geolocation.");
	}

	function sendEmail() {
        const email = document.getElementById('email').value;
		const lat = document.getElementById('lat').value;
		const lng = document.getElementById('lng').value;

		// Send data to backend for sending the email
		fetch('http://localhost:3000/send-email', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				email: email,
				lat: lat,
				lng: lng
			}),
		})
		.then(response => response.text())
		.then(data => {
			alert(data); // Show success message
		})
		.catch(error => {
			console.error('Error:', error);
			alert('Failed to send email');
		});
	}

	// Simulating coordinates selection from Google Maps (for demo purposes)
	document.getElementById('lat').value = localStorage.getItem("latstore"); // Example latitude (San Francisco)
	document.getElementById('lng').value = localStorage.getItem("lngstore"); // Example longitude
	
// Function to send email with coordinates
function sendEmail() {
    const email = document.getElementById('email').value;
    const lat = document.getElementById('lat').value;
    const lng = document.getElementById('lng').value;

    // Send data to backend for sending the email
    //yes
    fetch('https://hackathon-nasa-landsat.onrender.com/send-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            lat: lat,
            lng: lng
        }),
    })
    .then(response => response.text())
    .then(data => {
        alert(data); // Show success message
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send email');
    });
}

//test