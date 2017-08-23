/*global ko:false */
/*global google:false */
/*global $:false */
var locationsSeeder = [{
    name: 'Wave Broadband HQ',
    wiki: 'Wave Broadband',
    lat: 47.6779,
    lng: -122.1981
}, {
    name: 'Tableau Software Kirkland',
    wiki: 'Tableau Software',
    lat: 47.6786,
    lng: -122.1966
}, {
    name: 'Google Kirkland',
    wiki: 'Google',
    lat: 47.6697,
    lng: -122.1978
}, {
    name: 'Starbucks - Downtown',
    wiki: 'Starbucks',
    lat: 47.6758,
    lng: -122.2066
}, {
    name: 'QFC - Park Place',
    wiki: 'QFC',
    lat: 47.6768,
    lng: -122.2003
}];
var map;
var Location = function(data) {
        var self = this;
        this.name = data.name;
        this.lat = data.lat;
        this.lng = data.lng;
        this.description = "";
        this.selected = ko.observable(false);
        this.marker = new google.maps.Marker({
            title: data.name,
            map: map,
            position: new google.maps.LatLng(data.lat, data.lng)
        });
        this.infoWindow = new google.maps.InfoWindow({
            content: this.name
        });
        var wp_api = 'https://en.wikipedia.org/w/api.php?format=json&action=query&origin=*&prop=extracts&exintro=&explaintext=';
        $.getJSON({
            url: wp_api,
            data: {
                titles: data.wiki
            }
        }).done(function(data) {
            $.each(data.query.pages, function(i, item) {
                // Shortens to first sentence.
                self.description = item.extract.split('. ', 1) + '.';
            });
        }).fail(function() {
            alert("There was an error retrieving data from Wikipedia. Please try again.");
        });
        this.showMarker = function(state) {
            if (state) self.marker.setMap(map);
            else self.marker.setMap(null);
        };
    };

function AppViewModel() {
    'use strict';
    var self = this;
    this.textbox = ko.observable("");
    this.search = ko.observable("");
    this.locations = ko.observableArray([]);
    this.filteredLocations = ko.computed(function() {
        if (!self.search()) {
            self.locations().forEach(function(loc) {
                loc.showMarker(true);
            });
            return self.locations();
        } else {
            return ko.utils.arrayFilter(self.locations(), function(loc) {
                var result = loc.name.toLowerCase().includes(self.search().toLowerCase());
                loc.showMarker(result);
                return result;
            });
        }
    });
    this.select = function(location) {
        self.textbox(location.description);
        self.locations().forEach(function(loc) {
            loc.selected(false);
            loc.infoWindow.close(map, this);
        });
        location.selected(true);
    };
    this.click = function(location) {
        google.maps.event.trigger(location.marker, 'click');
    };
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: {
            lat: 47.6763491,
            lng: -122.2021082
        }
    });
    locationsSeeder.forEach(function(loc) {
        self.locations.push(new Location(loc));
    });
    self.locations().forEach(function(loc) {
        google.maps.event.addListener(loc.marker, 'click', function() {
            self.select(loc);
            loc.marker.setAnimation(google.maps.Animation.DROP);
            map.panTo(loc.marker.getPosition());
            loc.infoWindow.open(map, this);
        });
    });
    this.mapElem = document.getElementById('map');
}

function startApp() {
    ko.applyBindings(new AppViewModel());
}

function handleError() {
    alert('An error has occured loading Google Maps. Please try again later.');
}