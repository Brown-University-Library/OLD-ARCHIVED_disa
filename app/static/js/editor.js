var editor = (function () {
    'use strict';

    var initModule = function( $container ) {
        editor.relationships.initModule( $container );
    }

    return { initModule : initModule };
}());