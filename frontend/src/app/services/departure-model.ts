const MINUTES_IN_DAY = 1440;

export interface RawDeparture {
    from_scheduled_time: string;
    from_estimated_time: string;
    to_scheduled_time: string;
    to_estimated_time: string;
    to_crs: string;
    platform: string;
    length: string;
}

export class Departure implements RawDeparture {
    readonly fromDelayedMinutes: number;
    readonly toDelayedMinutes: number;

    constructor(
        readonly from_scheduled_time: string,
        readonly from_estimated_time: string,
        readonly to_scheduled_time: string,
        readonly to_estimated_time: string,
        readonly to_crs: string,
        readonly platform: string,
        readonly length: string,
        readonly is_cancelled_or_permanently_delayed: boolean,
        readonly isFromTimeDelayed: boolean,
        readonly isToTimeDelayed: boolean,
    ) {
        this.fromDelayedMinutes = getDelayMinutes(from_scheduled_time, from_estimated_time);
        this.toDelayedMinutes = getDelayMinutes(to_scheduled_time, to_estimated_time);
    }
}

export function convertRawDurationToDuration(rawDeparture: RawDeparture): Departure {
    return new Departure(
        rawDeparture.from_scheduled_time,
        getEstimatedTime(rawDeparture.from_scheduled_time, rawDeparture.from_estimated_time),
        rawDeparture.to_scheduled_time,
        getEstimatedTime(rawDeparture.to_scheduled_time, rawDeparture.to_estimated_time),
        rawDeparture.to_crs,
        rawDeparture.platform,
        rawDeparture.length,
        rawDeparture.from_estimated_time == "Cancelled" || rawDeparture.from_estimated_time == "Delayed" || rawDeparture.to_estimated_time == "Cancelled" || rawDeparture.to_estimated_time == "Delayed",
        isFromTimeDelayed(rawDeparture),
        isToTimeDelayed(rawDeparture)
    )
}


function getEstimatedTime(scheduled_time: string, estimated_time: string): string {
    if (!estimated_time || estimated_time.toLowerCase() == "on time") {
        return scheduled_time;
    } else {
        return estimated_time;
    }
}

function isFromTimeDelayed(departure: RawDeparture): boolean {
    return (departure.from_scheduled_time == getEstimatedTime(departure.from_scheduled_time, departure.from_estimated_time))
}

function isToTimeDelayed(departure: RawDeparture): boolean {
    return (departure.to_scheduled_time == getEstimatedTime(departure.to_scheduled_time, departure.to_estimated_time))
}

function getDelayMinutes(scheduled_time: string, estimated_time: string): number {
    const scheduled_minutes = convertTimeToMinutes(scheduled_time);
    const estimated_minutes = convertTimeToMinutes(estimated_time);
    const delta = estimated_minutes - scheduled_minutes;
    // Handle delays that cross midnight
    return (MINUTES_IN_DAY + delta) % MINUTES_IN_DAY
}

export function convertTimeToMinutes(timeString: string): number {
    const elements = timeString.split(":")
    return parseInt(elements[0]) * 60 + parseInt(elements[1])
}
