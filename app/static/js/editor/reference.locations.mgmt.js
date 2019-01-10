class LocationMgmt {

  constructor(referenceId, source, $elem) {
    var $tbody = $('<tbody/>');
    var $tfoot = $('<tfoot/>');
    $elem.append($tbody).append($tfoot);

    this._reference = referenceId;
    this._source = source;
    this._$root = $elem;
    this._$body = $tbody;
    this._$foot = $tfoot;
    this._data = [];
    this._$root[0].addEventListener('click', this);
  }

  load() {
    this._source.getLocations(this._reference);
  }

  loadData(data) {
    this._data = data.locations;
    this.populate();
  }

  swapIndex(first, second) {
    var front, back, block;
    if ( (first > second) || (second == 0) || (second + 1 > this._data.length) ) {
      return;
    }
    front = this._data.slice(0, first);
    back = this._data.slice(second + 1, this._data.length);
    block = [ this._data[second], this._data[first] ];
    this._data = front.concat(block).concat(back);
    this.populate();
  }

  populate() {
    var $row_add, $td_add, $btn_add;

    this._$body.empty();

    for (var i=0; i < this._data.length; i++) {
      var obj, loc_id, loc_name, $row;
      
      obj = this._data[i];
      loc_id = obj.id;
      loc_name = obj.name;

      $row = this.makeRow(loc_id, loc_name, i);
      this._$body.append($row);
    }

    $row_add = $('<tr/>');
    $td_add = $('<td/>');
    $btn_add = $('<button/>',
      { 'class': 'btn btn-primary add-loc',
        'text': 'Additional location' });
    $row_add.append($td_add.append($btn_add)).append($('<td/>'))
      .append($('<td/>')).append($('<td/>')).append($('<td/>'));
    this._$body.append($row_add);
  }

  makeRow( locId, locName, locIdx ) {
    var
      $row, 
      $td_name, $td_del, $td_up, $td_down,
      $button_del, $button_up, $button_down,
      $span_del, $span_up, $span_down;

    $row = $('<tr/>',
        {'class': 'location-row',
         'data-loc-id': locId,
         'data-loc-idx': locIdx });
    $td_name = $('<td/>').append(
      $('<input/>', {
        'class': 'form-control location-name',
        'type': 'text',
        'value': locName }) );
    $td_del = $('<td/>');
    $td_up = $('<td/>');
    $button_up = $('<button/>',
      { 'class': (locIdx == 0) ? 'btn btn-light loc-up' : 'btn btn-light move-loc loc-up',
        'data-loc-idx': locIdx });
    $span_up = $('<span/>',
      { 'class': (locIdx == 0) ? 'fas fa-ban no-loc' : 'fa fa-arrow-up' });
    $td_down = $('<td/>');
    $button_down = $('<button/>',
      { 'class': (locIdx == this._data.length - 1) ? 'btn btn-light loc-down' : 'btn btn-light move-loc loc-down',
        'data-loc-idx': locIdx });
    $span_down = $('<span/>',
      { 'class': (locIdx == this._data.length - 1) ? 'fas fa-ban no-loc' : 'fa fa-arrow-down' });
    $button_del = $('<button/>',
      { 'class': 'btn btn-danger del-loc',
        'data-loc-idx': locIdx });
    $span_del = $('<span/>', {'class': 'fas fa-times-circle'});
    $row.append($td_name)
        .append($td_up.append($button_up.append($span_up)))
        .append($td_down.append($button_down.append($span_down)))
        .append($td_del.append($button_del.append($span_del)));
    return $row;
  }

  addRow() {
    var new_loc = { id: 'new', name: ''};
    this._data.push(new_loc);
    this.populate();
  }

  deleteLocation(locIdx) {
    if (this._data.length == 1) {
      var new_loc = { id: 'new', name: ''};
      this._data = [ new_loc ];
    }
    else {
      this._data.splice(locIdx, 1);
    }
    this.populate();
  }

  handleEvent(event) {
    let target = event.target;
    switch(event.type) {
      case "click":
        if (target.classList.contains('del-loc')) {
          var loc_idx = parseInt(target.getAttribute('data-loc-idx'));
          this.deleteLocation(loc_idx);
        }
        else if (target.classList.contains('move-loc')) {
          var loc_idx = parseInt(target.getAttribute('data-loc-idx'));
          if (target.classList.contains('loc-up')) {
            this.swapIndex(loc_idx - 1, loc_idx);
          } else if (target.classList.contains('loc-down')) {
            this.swapIndex(loc_idx, loc_idx + 1);
          }
        }
        else if (target.classList.contains('add-loc')) {
          this.addRow();
        }
        return;
      default:
        return;
    }
  }
}