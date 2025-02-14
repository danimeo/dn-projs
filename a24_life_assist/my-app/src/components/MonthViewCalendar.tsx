import React, { useState } from 'react';
import { Button } from '@fluentui/react-components';
import MonthView from './MonthView';
import './MonthViewCalendar.css';

const MonthViewCalendar: React.FC = () => {
    const initMonth = new Date(2024, 8);
    let months = [initMonth];
    for(let i=1; i<6; i++){
        months = [...months, new Date(initMonth.getFullYear(), initMonth.getMonth() + i)];
    }
    const [currentMonths, setCurrentMonths] = useState(months);
    // console.log(currentMonths);

    const nextMonth = () => {
        let months = Array.from(currentMonths);
        for(let i=0; i<months.length; i++){
            months[i] = new Date(months[i].getFullYear(), months[i].getMonth() + 1);
        }
        setCurrentMonths(months);
      };
    
    const prevMonth = () => {
        let months = Array.from(currentMonths);
        for(let i=0; i<months.length; i++){
            months[i] = new Date(months[i].getFullYear(), months[i].getMonth() - 1);
        }
        setCurrentMonths(months);
    };

  return (
    <div>
        <div className="flex-row">
        {
            currentMonths.map((item, index) => (
                <MonthView currentMonth={item} />
            ))
        }
        </div>
        <div className='buttons'>
            <Button appearance="primary" onClick={prevMonth}>上一页</Button>
            <Button appearance="primary" onClick={nextMonth}>下一页</Button>
        </div>
    </div>
  );
};

export default MonthViewCalendar;