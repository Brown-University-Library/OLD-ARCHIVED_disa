class ReferenceSource extends Source {

  // createReferent(data) {
  //   var endpoint = this.endpoints.createReferent;
  //   this.request(endpoint, 'POST', 'referentSaved', data);
  // }

  // updateReferent(rntId, data) {
  //   var endpoint = this.endpoints.updateReferent + rntId;
  //   this.request(endpoint, 'PUT', 'referentSaved', data);
  // }

  // deleteReferent(rntId) {
  //   var endpoint = this.endpoints.deleteReferent + rntId;
  //   this.request(endpoint, 'DELETE', 'referentDeleted');
  // }

  createReference(data) {
    var endpoint = this.endpoints.updateReference;
    this.request(endpoint, 'POST', 'referenceSaved', data);
  }

  updateReference(data, refId) {
    var endpoint = this.endpoints.updateReference + refId;
    this.request(endpoint, 'PUT', 'referenceSaved', data);
  }
}