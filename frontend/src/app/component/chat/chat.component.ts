import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule} from "@angular/forms";
import {Message} from "../../common/message";
import {MessageService} from "../../service/message-service";

@Component({
  selector: 'app-chat',
  standalone: true,
    imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {
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
