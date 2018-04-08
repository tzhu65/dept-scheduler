import * as React from "react";

export class GenerateScheduleInput extends React.Component<null, { text: string }> {

  constructor(props: any) {
    super(props);
    this.state = { text: "test" };
    this.onSubmit = this.onSubmit.bind(this);
  }

  public onSubmit(e: any) {
    e.preventDefault();
    $.ajax({
      url: "generateSchedule",
      type: "POST",
      data: new FormData(($("#generate-schedule-id")[0] as HTMLFormElement)),
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
          id="generate-schedule-id"
          action="/generateSchedule"
          method="post"
          encType="multipart/form-data"
          onSubmit={this.onSubmit}
        >
          Select schedule to upload:
          <input id="vs-courses-input-id" type="file" name="courses" />
          <br />
          Select preferences to upload:
          <input id="vs-people-input-id" type="file" name="people" />
          <br />
          Select faulty hours to upload:
          <input id="vs-faculty-input-id" type="file" name="faculty" />
          <input type="submit" value="Upload" name="submit" />
        </form>
        <div>
          {this.state.text}
        </div>
      </div>
    );
  }
}
