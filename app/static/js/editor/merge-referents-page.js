class Source {

  constructor($elem, endpoints) {
    this._$root = $elem;
    this.urls = endpoints;
  }

  get( endpoint, callback, payload=null ) {
    $.ajax({
      type: "GET",
      data: payload,
      dataType: "json",
      url: endpoint,
      context: this,
      success: function( data ) {
        this._$root.trigger( callback, data );
      }
    });
  }

  post( endpoint, payload, callback ) {
    $.ajax({
      type: "POST",
      data: JSON.stringify(payload),
      contentType: "application/json",
      dataType: "json",
      url: endpoint,
      success: function( data ) {
        this._app[callback]( data );
      }
    });
  }

  put( endpoint, payload, callback ) {
    $.ajax({
      type: "PUT",
      data: JSON.stringify(payload),
      contentType: "application/json",
      dataType: "json",
      context: this,
      url: endpoint,
      success: function( data ) {
        this._app[callback]( data );
      }
    });
  }

  destroy( endpoint, payload, callback ) {
    $.ajax({
      type: "DELETE",
      data: JSON.stringify(payload),
      contentType: "application/json",
      dataType: "json",
      url: endpoint,
      success: function( data ) {
        callback( data );
      }
    });
  }

  getPageConfig( rntId ) {
    this.get(this.urls['landing'] + rntId, 'config_retrieved');
  }

  searchPeople( filters ) {
    this.get(this.urls['people'], 'search_completed', filters);
  }

  create_reference( data ) {
    
  }

  update_reference( refId, data ) {

  }

  list_referents( refId ) {

  }

  read_referent( rntId ) {

  }

  create_referent( data ) {
    
  }

  update_referent( rntId, data ) {

  }

  delete_referent( rntId ) {

  }
}

class ReferentRow {
  
}

class ReferentManager {
  constructor($elem) {
    this._$root = $elem;
    this.$rows = [];
    this.templates = {};    
    this.setTemplates();
  }

  init( rowData ) {
    for (var i=0; i < rowData.length; i++) {
      
    }
  }

  setTemplates() {
    let tmpl_map = this.templates;
    let $templates = this._$root.find('template');
    $templates.each(function() {
      let $tmpl = $( $(this).prop('content') ).children().first();
      $tmpl.detach();
      tmpl_map[$tmpl.attr('id')] = $tmpl;
      $tmpl.attr('id', '');
      $(this).remove();
    });
  }

  show() {
    this._$root.prop('hidden', false);
  }

  hide() {
    this._$root.prop('hidden', true);
  }

  activateRow( rowId ) {
  }

  deactivateRow( rowId ) {
  }

  deactivate() {

  }
}

class FilterRow {
  constructor($elem, rowData) {
    this._$root = $elem;
    this._$filter_val = $elem.find('.search-referents-filter-value');
    this._$filter_field = $elem.find('.search-referents-filter-field');

    this._$root.attr('data-field', rowData.field_name);
    this._$root.attr('data-field-value', rowData.filter_value);
    this._$filter_val.text(rowData.filter_value);
    this._$filter_field.text(rowData.field_name);
  }

  getRoot() {
    return this._$root;
  }

  read() {
    let filter_data = {};
    filter_data.name = this._$root.attr('data-field');
    filter_data.value = this._$root.attr('data-field-value');
    return filter_data;
  }

  isValid() {
    return (this._$root.attr('data-field') != '' && this._$root.attr('data-field-value') != '');
  }

  isEqual( other ) {
    let f1 = this.read();
    let f2 = other.read();
    return ( f1.name === f2.name );
  }
}

class FilterMaker {
  constructor($elem, $optionTemplate) {
    this._$root = $elem;
    this._$opt_tmpl = $optionTemplate;
    this._$field_val = $elem.find('.search-referents-input-value');
    this._$field_select = $elem.find('.search-referents-select-field');
  }

  loadOptions( options ) {
    for (var i=0; i < options.length; i++) {
      let opt_data = options[i];
      let $opt = this._$opt_tmpl.clone();
      $opt.attr('value', opt_data.id);
      $opt.html(opt_data.name);
      this._$field_select.append($opt);
    }
  }

  read() {
    let filter_data = {};
    filter_data.field_name = this._$field_select.find(':selected').text();
    filter_data.field_value = this._$field_select.val();
    filter_data.filter_value = this._$field_val.val();

    return filter_data;
  }

  reset() {
    this._$field_val.val('');
  }
}

class ReferentSearch {
  constructor($elem) {
    this._$root = $elem;
    this.$filter_list = $elem.find('#filter_list');
    this.filter_rows = [];
    this.templates = {};
    this.updated = false;

    this.setTemplates();
    this.filter_maker = new FilterMaker($elem.find('#filter_maker'),
      this.templates.filter_option)
  }

  setTemplates() {
    let tmpl_map = this.templates;
    let $templates = this._$root.find('template');
    $templates.each(function() {
      let $tmpl = $( $(this).prop('content') ).children().first();
      $tmpl.detach();
      tmpl_map[$tmpl.attr('id')] = $tmpl;
      $tmpl.attr('id', '');
      $(this).remove();
    });
  }

  init( data ) {
    this.filter_maker.loadOptions( data );
  }

  addFilter() {
    let filter = new FilterRow( this.templates.search_filter_row.clone(),
      this.filter_maker.read() );
    if (!this.hasFilter(filter) && filter.isValid()) {
      this.filter_rows.push(filter);
      this.$filter_list.append( filter.getRoot() )
      this.updated = true;
    } else {
      this.updated = false;
    }
    this.filter_maker.reset();
  }

  hasFilter( filter ) {
    for (var i=0; i < this.filter_rows.length; i++) {
      if ( this.filter_rows[i].isEqual(filter) ) {
        return true;
      }
    }
    return false;
  }

  removeFilter( rowIdx ) {

  }

  readFilters() {
    let filter_data = [];
    for (var i=0; i < this.filter_rows.length; i++) {
      filter_data.push(this.filter_rows[i].read())
    }
    return filter_data;
  }
}

class MergeReferentsPage {

  constructor($elem, source, rntId) {
    this._$root = $elem;
    this.referent_id = rntId;
    this.data = {};

    this.source = source;
    this.referent_search = new ReferentSearch($elem.find('#referent_search'));
    // this.referent_results = new ReferentSearchResults(
    //   $elem.find('#referent_search_results'));

    this.registerEvents();
  }

  initialPageLoad( data ) {
    this.referent_search.init( data.filter_fields );
    // this.referent_results.load_results( data.referents );
  }

  registerEvents() {
    let that = this;

    this._$root.on('click', 'button', function(e){
      e.preventDefault();
      let $btn = $( this );

      switch ( true ){
        case $btn.hasClass('filter-referents'):
          that.referent_search.addFilter();
          if ( that.referent_search.updated ) {            
            that.source.searchPeople( that.referent_search.readFilters() );
          }
          break;
        case $btn.hasClass('cancel-edit-reference'):
          break;
        case "save_reference":
          break;
        case "edit_referent":
          break;
        case "cancel_edit_referent":
          break;
        case "save_referent":
          break;
        case "delete_referent":
          break
      }

    });
    this._$root.on('config_retrieved', function(e, data){
      that.initialPageLoad( data );
    });
    this._$root.on('search_completed', function(e, data){
      console.log( data );
    });
  }

  init() {
    this.source.getPageConfig( this.referent_id );
  }
}