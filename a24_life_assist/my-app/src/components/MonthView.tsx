import React from 'react';

type MonthProps = { currentMonth: Date };

const MonthView: React.FC<MonthProps> = ({currentMonth}) => {
    const daysInMonth = (year: number, month: number): number => new Date(year, month + 1, 0).getDate();
    const firstDayOfMonth = (year: number, month: number): number => new Date(year, month, 1).getDay();
  
    

    return (
        <div>
            <div>
            <h3>{currentMonth.toLocaleString('default', { month: 'long' })}, {currentMonth.getFullYear()}</h3>
            
            <table>
                <thead>
                <tr>
                    <th>Sun</th>
                    <th>Mon</th>
                    <th>Tue</th>
                    <th>Wed</th>
                    <th>Thu</th>
                    <th>Fri</th>
                    <th>Sat</th>
                </tr>
                </thead>
                <tbody>
                {Array.from({ length: Math.ceil((daysInMonth(currentMonth.getFullYear(), currentMonth.getMonth()) + firstDayOfMonth(currentMonth.getFullYear(), currentMonth.getMonth())) / 7) }, (_, rowIndex) => (
                    <tr key={rowIndex}>
                    {Array.from({ length: 7 }, (_, colIndex) => {
                        const day = rowIndex * 7 + colIndex - firstDayOfMonth(currentMonth.getFullYear(), currentMonth.getMonth()) + 1;
                        if (day > 0 && day <= daysInMonth(currentMonth.getFullYear(), currentMonth.getMonth())) {
                        return <td key={colIndex}>{day}</td>;
                        }
                        return <td key={colIndex}></td>;
                    })}
                    </tr>
                ))}
                </tbody>
            </table>
            </div>
        </div>
      );
    };
    
    export default MonthView;