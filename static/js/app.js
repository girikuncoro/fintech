'use strict';

var API_CALL = '/api/v1.0/data/country/';

var modernMobile = angular.module('modernMobile', ['ui.bootstrap','ngRoute','transactionGridMod']);

modernMobile.controller('modernMobileCtrl', ["$scope", "$http","$log","gridSvc","$rootScope", function($scope,$http,$log,gridSvc,$rootScope) {
	$scope.transactionFile = "";
	$scope.upload = function(form) {
		console.log($scope.transactionFile);
		console.log(form);
		$rootScope.$emit("reload-grid-again");
	}
	
	$scope.readFileData = function(fileName) {
		var fileReader = new FileReader();
		fileReader.onload = function(event) {
			$scope.b
			var data = event.target.result;
			//console.log(data);
		//	gridSvc.refreshGridData(data);
			$rootScope.$emit("reload-grid",data);
		}
		fileReader.readAsText(fileName);
	}
	
}]);


modernMobile.directive("fileHandler",[function() {
	return {
		require:"ngModel",
		restrict : "A",
		link : function($scope,element,attrs,ngModel) {
			element.bind("change",function(changeEvent){
				//console.log(changeEvent);
				var filename = changeEvent.target.files[0];
				$scope.readFileData(filename);
			})
		}
	}
}])

//myapp.factory('loginService',['$http',function($http) {
//	var login;
//	login = {
//		'login' : function(username,pass) {
//			$http({
//				'method' : 'POST'
//			}).then(function(success) {
//				
//			}, function(error){
//				
//			})
//		}
//	}
//	
//	return login;
//
//}])
//

