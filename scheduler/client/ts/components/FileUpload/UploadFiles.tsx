import * as React from "react";

export class UploadFiles extends React.Component<null, { text: string }> {

  constructor(props: any) {
    super(props);
    this.state = { text: "test" };
    this.onSubmit = this.onSubmit.bind(this);
  }

  public onSubmit(e: any) {
    e.preventDefault();
    $.ajax({
      url: "verifySchedule",
      type: "POST",
      data: new FormData(($("#verify-schedule-id")[0] as HTMLFormElement)),
      cache: false,
      contentType: false,
      processData: false,

      // Custom XMLHttpRequest
      xhr: () => {
        const myXhr = $.ajaxSettings.xhr();
        if (myXhr.upload) {
          // For handling the progress of the upload
          myXhr.upload.addEventListener("progress", (event: any) => {
            if (event.lengthComputable) {
              console.log(event.loaded, event.total);
            }
          }, false);
        }
        return myXhr;
      },

      success: (data: any, status: string, xhr: JQuery.jqXHR) => {
        this.setState({text: `JSON data response: ${JSON.stringify(data, null, 2)}`});
      },
      error: (xhr: JQuery.jqXHR, status: string, error: string) => {
        this.setState({text: `ERROR\t${status}\t${error}`});
      },
    });
  }

  public render() {
    return (
      <div>
        <form
          id="verify-schedule-id"
          action="/verifySchedule"
          method="post"
          encType="multipart/form-data"
          onSubmit={this.onSubmit}
        >
          Select courses to upload:
          <input id="vs-courses-input-id" type="file" name="courses" />
          <br />
          Select schedule to upload:
          <input id="vs-schedule-input-id" type="file" name="schedule" />
          <input type="submit" value="Upload Image" name="submit" />
        </form>
        <div>
          {this.state.text}
        </div>
      </div>
    );
  }
}
