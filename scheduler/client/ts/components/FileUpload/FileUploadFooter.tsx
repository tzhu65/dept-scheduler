import * as React from "react";

import { IAPICallerStoreState, APICallerStore } from "../../stores/APICallerStore";

export class FileUploadFooter extends React.Component<null, IAPICallerStoreState> {

  constructor(props: any) {
    super(props);
    this.onChange = this.onChange.bind(this);
  }

  public componentWillMount() {
    this.setState(APICallerStore.getState());
  }

  public componentDidMount() {
    APICallerStore.listen(this.onChange);
  }

  public componentWillUnmount() {
    APICallerStore.unlisten(this.onChange);
  }

  public onChange(state: IAPICallerStoreState) {
    this.setState(state);
  }

  public render() {
    return (
      <div className="navbar fixed-bottom">
        Time: {this.state.delay}
      </div>
    );
  }
}
