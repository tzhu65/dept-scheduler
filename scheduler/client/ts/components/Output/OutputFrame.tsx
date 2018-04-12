import * as React from "react";

import { IOutputStoreState, OutputStore } from "../../stores/OutputStore";

import { OutputOverlay } from "./OutputOverlay";

export class OutputFrame extends React.Component<null, IOutputStoreState> {

  constructor(props: any) {
    super(props);
    this.onChange = this.onChange.bind(this);
  }

  public componentWillMount() {
    this.setState(OutputStore.getState());
  }

  public componentDidMount() {
    OutputStore.listen(this.onChange);
  }

  public componentWillUnmount() {
    OutputStore.unlisten(this.onChange);
  }

  public onChange(state: IOutputStoreState) {
    this.setState(state);
    const outputDiv = document.getElementById("output-log-id");
    outputDiv.scrollTop = outputDiv.scrollHeight;
  }

  public render() {
    return (
      <div>
        <div id="output-log-id" className="scrollable">
          <OutputOverlay />
          {this.state.logs.map((log: string, index: number) => {
            return <div key={index}>{log}</div>;
          })}
        </div>
      </div>
    );
  }
}
