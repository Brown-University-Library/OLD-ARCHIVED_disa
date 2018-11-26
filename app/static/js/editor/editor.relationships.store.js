class RelationshipStore {

  constructor($elem) {
    this._$root = $elem;
    this._data = [];
  }

  compareData(d1, d2) {
    if (d1.data.sbj.name < d2.data.sbj.name) { 
      return -1;
    }
    if (d1.data.sbj.name > d2.data.sbj.name) {
      return 1;
    }
    if (d1.data.rel.name < d2.data.rel.name) { 
      return -1;
    }
    if (d1.data.rel.name > d2.data.rel.name) {
      return 1;
    }
    if (d1.data.obj.name < d2.data.obj.name) { 
      return -1;
    }
    if (d1.data.obj.name > d2.data.obj.name) {
      return 1;
    }
    return 0;
  }

  load( data ) {
    var curr_sbj, curr_rel;

    this._$root.empty();
    this._data = data.sort(this.compareData);

    for (var i=0; i < this._data.length; i++) {
      let obj = this._data[i];
      let rel_id = obj.id;
      let rel_data = obj.data;
      let $row = this.makeRow(rel_data, rel_id,
        (rel_data.sbj.id===curr_sbj), (rel_data.rel.id===curr_rel));
      this._$root.append($row);
      curr_sbj = rel_data.sbj.id;
      curr_rel = rel_data.rel.id;
    }
  }

  makeRow( data, relId, sbjIsRepeat, relIsRepeat ) {
    var
      $row, $td_sbj, $td_rel, $td_obj,
      $td_del, $button, $span;
    $row = $('<tr/>');
    $td_sbj = $('<td/>', { 'text': sbjIsRepeat ? '' : data.sbj.name });
    $td_rel = $('<td/>', { 'text': relIsRepeat ? '' : data.rel.name });
    $td_obj = $('<td/>', { 'text': data.obj.name });
    $td_del = $('<td/>');
    $button = $('<button/>',
      { 'class': 'btn btn-danger del-rel',
        'data-rel-id': relId });
    $span = $('<span/>', {'class': 'fas fa-times-circle', 'html' : '\&times\;'});
    $row.append($td_sbj).append($td_rel).append($td_obj).append(
      $td_del.append($button.append($span)));
    return $row;
  }

  getRow( idx ) {
    return this._data[idx];
  }
}