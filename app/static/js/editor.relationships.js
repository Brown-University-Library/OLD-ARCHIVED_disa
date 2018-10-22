editor.relationships = (function( $container ) {
  var
    configMap, stateMap, jqueryMap,

    initModule, setJqueryMap,

    setListeners, loadData;

    configMap = {
      main_html : String()
        + '<table id="matrix">'
          + '<tbody>'
          + '</tbody>'
        + '</table>'
    }

    stateMap = {
      $root: undefined,
      $ref_rels: [],
      $rels : [],
      $rel_invrs: {},
      $referents : {}
    };

    jqueryMap = {};

    setJqueryMap = function() {
      var $root = stateMap.$root;

      $root.append(configMap.main_html);

      jqueryMap = {
        $root : $root,
        $matrix : $root.find('#matrix')
      }

      return true;
    }

    setListeners = function() {
      $( jqueryMap.$root ).on('click', '.add-relationship', function(e) {
        e.preventDefault();
        console.log( $(this).closest('person-row').attr('data-person-id') );
      });
    }

    loadData = function ( data ) {
      // stateMap.ref_rels = data['referent_relationships'];
      stateMap.referents = data['referents'];
      stateMap.rels = data['relationships'];
      // stateMap.rel_invrs = data['inverse_relationships'];

      console.log(stateMap);
    }

    initModule = function( $container ) {
        stateMap.$root = $container;
        stateMap.section_id = $container.attr('data-section-id');
        setJqueryMap();
        setListeners();

        $.ajax({
          dataType: "json",
          url: 'localhost:5000/data/relationships/' + stateMap.section_id,
          success: function( data ) {
            loadData( data );
          }
        });
    }

    return { initModule: initModule };
}());