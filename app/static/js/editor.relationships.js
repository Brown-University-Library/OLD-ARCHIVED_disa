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

    dataMap = {
      rels : []
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

    //http://adripofjavascript.com/blog/drips/object-equality-in-javascript.html
    function isEquivalent(a, b) {
      // Create arrays of property names
      var aProps = Object.getOwnPropertyNames(a);
      var bProps = Object.getOwnPropertyNames(b);

      // If number of properties is different,
      // objects are not equivalent
      if (aProps.length != bProps.length) {
          return false;
      }

      for (var i = 0; i < aProps.length; i++) {
          var propName = aProps[i];

          // If values of same property are not equal,
          // objects are not equivalent
          if (a[propName] !== b[propName]) {
              return false;
          }
      }

      // If we made it this far, objects
      // are considered equivalent
      return true;
    }

    nullData = function() {
      return {};
    }

    mintData = function(s,p,o) {
      return {'sbj':s, 'prop': p,'val':o};
    }

    makeInverseData = function( data, inverseMap ) {
      var prop, inv_prop, inv_data;

      prop = data.property;
      inv_prop = inverseMap.prop;
      if (inv_prop === undefined) {
        return nullData();
      }

      inv_data = mintData(data.val, inv_prop, data.sbj);
      return inv_data;
    }

    dataInGraph = function ( data, graphData ) {
      for (var i; i < graphData.length; i++ ) {
        if ( isEquivalent(data, graphData[i]) ) {
          return true;
        }
        return false;
      }
    }

    dataSubtract = function( toRemove, removeFrom) {
      var updated = removeFrom.slice(0);

      for (var i; i < toRemove.length; i++ ) {
        updated = updated.filter(function(e) {
          return !isEquivalent(e, toRemove[i])
        });
      }

      return updated;
    }

    updateGraph = function( data, graph, remove=false ) {
      var update_data, inv_data;

      update_data = [];
      if ( ( !remove && !dataInGraph(data, graph.data) )
          || ( remove && dataInGraph(data, graph.data) ) ) {
        update_data.push[data];
      }

      inv_data = makeInverseData(data, graph.inverse_lookup);
      if ( inv_data !== nullData() &&
          ( ( !remove && !dataInGraph(data, graph.data) )
          || ( remove && dataInGraph(data, graph.data) ) ) ) {
        update_data.push[inv_data];
      }

      if (update_data.length > 0) {
        if (remove) {
          graph.data = dataSubtract(update_data, graph.data);
        } else {
          graph.data.push(...to_add);
        }
      }
      return graph;
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

    pivotGraphToRows = function ( graph ) {
      var pivot = {'sbj': [], 'prop': [], 'val': []};

      for (let i=0; i < graph.data.length; i++) {
        let data = graphData[i];
        let sbj = { 'id': data['sbj'], 'display': graph.node_names[data['sbj']] };
        let prop = { 'id': data['prop'], 'display': graph.edge_names[data['prop']] };
        let val = { 'id': data['val'], 'display': graph.node_names[data['val']] };
        pivot.sbj.push(sbj)
      }
    }

    makeSelect = function ( objectArray ) {
      var $select;

      $select = $('<select/>');
      for (let i=0; i < objectArray.length; i++) {
        let data = objectArray[i];
        let $opt = $('<option/>', {'value': data.id, 'text': data.name });
        $select.append($opt);
      }

      return $select;
    }

    appendAddRow = function ( domMap, graph ) {
      var $matrix = domMap.$matrix;

      $row = $('<tr/>', {
        'class'     : 'matrix-row',
        'data-sbj'  : '',
        'data-prop'  : '',
        'data-val'  : ''
      });
      $td_sbj = $('<td/>');
      $select_sbj = makeSelect(graph.nodes);
      $td_prop = $('<td/>');
      $select_prop = makeSelect(graph.edges);
      $td_val = $('<td/>');
      $select_val = makeSelect(graph.nodes);
      $td_button = $('<td/>');
      $button = $('<button/>', { 
        'type'  : 'button',
        'class' : 'btn btn-primary',
        'html'  : '\&plus\;'
      });
      $td_sbj.append($select_sbj);
      $td_prop.append($select_prop);
      $td_val.append($select_val);
      $td_button.append($button);
      $row.append($td_sbj).append($td_prop)
        .append($td_val).append($td_button);
      $matrix.append($row);

      return true;
    } 

    refreshMatrixData = function () {
      stateMap.graph.data.forEach( function(rel) {
        updateMatrixData(rel, jqueryMap,
          stateMap.graph.node_lookup, stateMap.graph.edge_lookup);
      });
      appendAddRow(jqueryMap, stateMap.graph);
    }

    getRowData = function( $row ) {
      var sbj, prop, val;

      sbj = $row.attr('data-sbj');
      prop = $row.attr('data-prop');
      val = $row.attr('data-val');

      return mintData(sbj, prop, val);
    }

    // addRowToTable = function()

    loadData = function ( data ) {
      // stateMap.ref_rels = data.referent_relationships;
      // stateMap.refs = data.referents;
      // stateMap.rels = data.relationships;
      // stateMap.ref_map = data.referent_lookup;
      // stateMap.rel_map = data.relationship_lookup;
      stateMap.graph = data.graph;

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