class CitationSource extends Source {

  deleteReference(refId) {
    var endpoint = this.endpoints.deleteReference + refId;
    this.request(endpoint, 'DELETE', 'referenceDeleted');
  }

  createCitation(data) {
    var endpoint = this.endpoints.createCitation;
    this.request(endpoint, 'POST', 'citationSaved', data);
  }

  updateCitation(data) {
    var endpoint = this.endpoints.updateCitation;
    this.request(endpoint, 'PUT', 'citationSaved', data);
  }
}