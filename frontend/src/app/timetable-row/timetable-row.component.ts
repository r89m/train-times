import {Component, EventEmitter, OnInit} from '@angular/core';
import {convertTimeToMinutes, Departure} from '../services/departure-model';
import {TimetableService} from '../services/timetable.service';
import {Observable, of} from "rxjs";

@Component({
    selector: 'app-timetable-row',
    templateUrl: './timetable-row.component.html',
    styleUrls: ['./timetable-row.component.css']
})
export class TimetableRowComponent implements OnInit {

    constructor(private readonly timetableService: TimetableService) {
    }

    pageLoadNowString = new Date().toLocaleString("en-GB", {hour: "numeric", minute: "numeric"});

    count = 1;

    refreshComplete = new EventEmitter<boolean>();

    departures: Observable<Departure[]> = of([]);

    ngOnInit(): void {
        this.departures = this.timetableService.getDepartures();
    }

    triggerDataReload(): void {
        this.count++;
        setTimeout(() => {
            this.dataReloaded()
        }, 3000);
    }

    dataReloaded(): void {
        this.refreshComplete.emit(true);
    }

    getTimeUntilFromTime(departure: Departure): number {
        const estimated_minutes = convertTimeToMinutes(departure.from_estimated_time)
        const now_minutes = convertTimeToMinutes(this.pageLoadNowString);
        const delta = estimated_minutes - now_minutes;

        // Handle values that cross the midnight boundary
        if (delta > -60) {
            return delta;
        } else {
            return delta + 1440
        }
    }
}
