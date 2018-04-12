import * as React from "react";
import * as ReactDOM from "react-dom";

import { init } from "./init";
import "./alt";
import "./actions/AppActions";
import "./stores/APICallerStore";
import "./stores/OutputStore";

import { Frame } from "./components/Frame";

export class MainApp extends React.Component<null, null> {
  public render() {
    return (
      <div>
        <Frame />
      </div>
    );
  }
}

init();

ReactDOM.render(
  <MainApp />,
  document.getElementById("main"),
);
