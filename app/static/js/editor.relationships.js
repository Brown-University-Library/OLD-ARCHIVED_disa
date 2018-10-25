editor.relationships = (function( $container ) {
  var
    configMap, stateMap, jqueryMap,

    initModule, setJqueryMap,

    setListeners, loadData;

    configMap = {
      main_html : String()
        + '<table class="table">'
          + '<tbody id="matrix">'
          + '</tbody>'
        + '</table>'
    }

    stateMap = {
      $root: undefined,
      refs : [],
      rels : [],
      ref_map : {},
      rel_map : {},
      ref_rels: [],
      rel_invrs: {}
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

    updateMatrixData = function ( dataObj, domMap,
      refMap, relMap ) {
      var $matrix = domMap.$matrix;

      $row = $('<tr/>', {
        'class'     : 'matrix-row',
        'data-sbj'  : dataObj.sbj,
        'data-prop'  : dataObj.prop,
        'data-val'  : dataObj.val
      });
      $td_sbj = $('<td/>', {'text': refMap[dataObj.sbj] });
      $td_prop = $('<td/>', {'text': relMap[dataObj.prop] });
      $td_val = $('<td/>', {'text': refMap[dataObj.val] });
      
      $row.append($td_sbj).append($td_prop).append($td_val);
      $matrix.append($row);

      return true;
    } 

    refreshMatrixData = function () {
      stateMap.ref_rels.forEach( function(rel) {
        updateMatrixData(rel, jqueryMap,
          stateMap.ref_map, stateMap.rel_map);
      });
    }

    loadData = function ( data ) {
      stateMap.ref_rels = data.referent_relationships;
      stateMap.refs = data.referents;
      stateMap.rels = data.relationships;
      stateMap.ref_map = data.referent_lookup;
      stateMap.rel_map = data.relationship_lookup;

      refreshMatrixData();
    }

    initModule = function( $container ) {
        stateMap.$root = $container;
        stateMap.section_id = $container.attr('data-section-id');
        setJqueryMap();
        setListeners();

        $.ajax({
          dataType: "json",
          url: '/data/relationships/' + stateMap.section_id,
          success: function( data ) {
            loadData( data );
          }
        });
    }

    return { initModule: initModule };
}());