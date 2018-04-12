import * as React from "react";

export class AboutInfo extends React.Component<null, null> {

  constructor(props: any) {
    super(props);
  }

  public render() {
    return (
      <div
        className="modal fade"
        id="about-info-modal"
        tabIndex={-1}
        role="dialog"
        aria-labelledby="exampleModalLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="aboutInfoTitle">Info</h5>
              <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body">
              To be written.
            </div>
          </div>
        </div>
      </div>
    );
  }
}
