class DISASource {

  constructor(baseURL) {
    this._base = baseURL;
    this._apps = {};
  }

  registerApp( name, app ) {
    this._apps[name] = app;
  }

  getREST( endpoint, callback ) {
    $.ajax({
      type: "GET",
      dataType: "json",
      url: endpoint,
      success: function( data ) {
        callback( data );
      }
    });
  }

  postREST( endpoint, payload, callback ) {
    $.ajax({
      type: "POST",
      data: JSON.stringify(payload),
      contentType: "application/json",
      dataType: "json",
      url: endpoint,
      success: function( data ) {
        callback( data );
      }
    });
  }

  delREST( endpoint, callback ) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      url: endpoint,
      success: function( data ) {
        callback( data );
      }
    });
  }

  getRelationships(sectionId) {
    let endpoint = this._base + `/data/sections/${sectionId}/relationships/`;
    let callback = this._apps['rel-mgmt'].setUp;
    this.getREST(endpoint, callback);
  }

  addRelationship(sectionId, obj) {
    let endpoint = this._base + `/data/relationships/`;
    let callback = this._apps['rel-mgmt'].setUp;
    this.postREST(endpoint, obj, callback);
  }

  deleteRelationship(relId) {
    let endpoint = this._base + `/data/relationships/${relId}`;
    let callback = this._apps['rel-mgmt'].setUp;
    this.delREST(endpoint, callback);
  }
}