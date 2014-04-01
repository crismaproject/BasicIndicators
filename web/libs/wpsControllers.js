var wpsApp = angular.module ("wpsApp", []);


wpsApp.controller ('wpsCtrl', function ($scope, $http) {
    $scope.wpsEndpoint = "https://pinguin2.ait.ac.at/~peter/indicators/pywps.cgi";  # test system
    # $scope.wpsEndpoint = "https://crisma.ait.ac.at/indicators/pywps.cgi";           # production system
    $scope.indicators = ["deathsIndicator", "seriouslyDeterioratedIndicator", "improvedIndicator", "lifeIndicator"];
    $scope.indicator = $scope.indicators[0];

    $scope.worldstateUrl = "http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/2";
});