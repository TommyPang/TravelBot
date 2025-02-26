import { Component } from '@angular/core';
import {
  ButtonDirective,
  ButtonGroupComponent,
  CarouselCaptionComponent,
  CarouselComponent,
  CarouselControlComponent,
  CarouselIndicatorsComponent, CarouselInnerComponent, CarouselItemComponent
} from "@coreui/angular";
import {NgForOf} from "@angular/common";
import {Router} from "@angular/router";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CarouselCaptionComponent,
    CarouselComponent,
    CarouselControlComponent,
    CarouselIndicatorsComponent,
    CarouselInnerComponent,
    CarouselItemComponent,
    NgForOf,
    ButtonGroupComponent,
    ButtonDirective
  ],
  templateUrl: './home.component.html',
  // styleUrl: './home.component.css'
})
export class HomeComponent {
  slides: any[] = new Array(6).fill({ id: -1, src: '', title: '', subtitle: '' });
  constructor(private router: Router) {
    this.slides[0] = {
      id: 0,
      src: './assets/山村梨花又一春.jpg',
      title: '山村梨花又一春',
      subtitle: '山村梨花又一春'
    };
    this.slides[1] = {
      id: 1,
      src: './assets/晨光里.jpg',
      title: '晨光里',
      subtitle: '晨光里'
    };
    this.slides[2] = {
      id: 1,
      src: './assets/树山之夜.jpg',
      title: '树山之夜',
      subtitle: '树山之夜'
    };
    this.slides[3] = {
      id: 1,
      src: './assets/树山之春.jpg',
      title: '树山之春',
      subtitle: '树山之春'
    };
    this.slides[4] = {
      id: 1,
      src: './assets/茶园.jpg',
      title: '茶园',
      subtitle: '茶园'
    };
    this.slides[5] = {
      id: 1,
      src: './assets/魅力山村.jpg',
      title: '魅力山村',
      subtitle: '魅力山村'
    };
  }
  toChat() {
    this.router.navigateByUrl("chat")
  }
}
