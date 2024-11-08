import { Injectable } from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {Observable} from "rxjs";
import {Message} from "../common/message";

@Injectable({
  providedIn: 'root'
})
export class MessageService {
  constructor(private httpClient: HttpClient) { }

  public sendMessage(msg: string): Observable<any> {
    let url = `${environment.apiUrl}/query`;
    return this.httpClient.post(url, {"prompt": msg});
  }
}
