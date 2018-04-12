import * as React from "react";

import { AppActions } from "../../actions/AppActions";

export class Navbar extends React.Component<null, null> {

  constructor(props: any) {
    super(props);
  }

  public render() {
    return (
      <div className="fixed-top transparent-navbar">
        <div className="row">
          <div className="col-sm-3 offset-sm-9">
            <div className="float-right clickable">
              <button
                type="button"
                className="btn btn-primary-transparent"
                data-toggle="modal"
                data-target="#about-info-modal"
              >
                <i className="fas fa-question" />
              </button>

              <button
                type="button"
                className="btn btn-primary-transparent"
                onClick={AppActions.clearOutput}
              >
                <i className="fas fa-times" />
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
