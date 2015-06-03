var slideshowApp = angular.module('slideshow', ['ui.router'])
    .config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('levs-main', {
                url: '/',
                views: {
                    'navigation': {
                        templateUrl: 'static/src/views/navigation.html'
                    },
                    'content': {
                        templateUrl: 'static/src/views/content.html'
                    }
                }
            });
    }])
    .run(['$state', function($state) {
        $state.go('levs-main');
    }]);
