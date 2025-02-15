import {Injectable} from '@angular/core';
import {convertRawDurationToDuration, Departure, RawDeparture} from './departure-model';
import {HttpClient} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {environment} from "../../environments/environment";

@Injectable({
    providedIn: 'root'
})
export class TimetableService {

    constructor(private readonly http: HttpClient) {
    }

    // TODO: Convert to Observable? Add reload trigger
    getDepartures(): Observable<Departure[]> {
        return this.http.get<RawDeparture[]>(`${environment.apiBaseUrl}timetable/ecr2clj,lbg`)
            .pipe(map(departures => {
                return departures.map(convertRawDurationToDuration)
            }));
    }
}
