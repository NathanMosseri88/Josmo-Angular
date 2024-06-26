import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  admin = new BehaviorSubject<boolean>(false)

  constructor() { }

  isLoggedIn(): boolean {
    return !!sessionStorage.getItem('user')
  }

  isAdmin():Observable<boolean> {
    return this.admin.asObservable()
  }

}
