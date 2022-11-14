import {Component, EventEmitter, Input, OnDestroy, OnInit, Output} from '@angular/core';
import {Subscription} from "rxjs";


const REFRESH_INTERVAL = 15;

@Component({
    selector: 'app-auto-refresh',
    templateUrl: './auto-refresh.component.html',
    styleUrls: ['./auto-refresh.component.css']
})
export class AutoRefreshComponent implements OnInit, OnDestroy {

    @Input("refreshComplete")
    refreshComplete?: EventEmitter<boolean>;

    @Output("onRefresh")
    onRefresh = new EventEmitter<void>();

    refreshCompleteSubscription?: Subscription;

    refreshEnabled = true;
    isRefreshing = false;
    refreshTimeoutHandle: any;
    secondsUntilRefresh = REFRESH_INTERVAL;

    constructor() {
    }

    ngOnInit(): void {
        this.resetCountdown();
        this.refreshCompleteSubscription = this.refreshComplete?.subscribe((value => {
            this.isRefreshing = false;
            this.resetCountdown();
        }))
    }

    ngOnDestroy() {
        this.refreshCompleteSubscription?.unsubscribe();
    }

    resetCountdown() {
        this.secondsUntilRefresh = REFRESH_INTERVAL;
        this.scheduleCountdown();
    }

    handleCountdown(): void {
        if (this.secondsUntilRefresh == 1) {
            this.triggerRefresh();
        } else {
            this.secondsUntilRefresh--;
            this.scheduleCountdown();
        }
    }

    scheduleCountdown() {
        if (!this.refreshEnabled || this.isRefreshing) {
            return
        }
        clearTimeout(this.refreshTimeoutHandle);
        this.refreshTimeoutHandle = setTimeout(() => {
            this.handleCountdown();
        }, 1000);
    }

    triggerRefresh(): void {
        if (this.refreshEnabled) {
            this.isRefreshing = true;
            this.onRefresh.emit();
        }
    }
}
