import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://localhost:5000/api'

  constructor(private http: HttpClient) { }

  login(data:any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, data)
  }

  getPresets(): Observable<any> {
    return this.http.get(`${this.apiUrl}/presets`)
  }

  savePreset(data: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/presets`, data)
  }

  sendProposalForm(data:any):Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/proposals`, data)
  }
   
}
