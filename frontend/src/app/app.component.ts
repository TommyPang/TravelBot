import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {Message} from "./common/message";
import {MessageService} from "./service/message-service";
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  public messages: Message[] = [];
  public newMessage: string = '';

  constructor(private messageService: MessageService) {}

  public async send_message() {
    let request: Message = new Message();
    request.from_user = true;
    request.content = this.newMessage;
    this.messages.push(request);
    this.messageService.sendMessage(this.newMessage).subscribe((res) => {
      let response: Message = new Message();
      response.content = res.message;
      response.from_user = false;
      this.messages.push(response);
      this.newMessage = "";
    });
  }
}
