import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html'
})
export class HomeComponent implements OnInit {

  constructor() {}

/*  constructor( private http: HttpClient) { 
    this.http.get("http://192.168.84.108:8080/servicios/cargas")
             .subscribe(articulos => {
              console.log(articulos);
             });
  }*/

  ngOnInit(): void {
  }

}
