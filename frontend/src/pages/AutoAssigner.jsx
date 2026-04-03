import React, { useState, useEffect } from 'react';
import { UserCheck, FileBarChart, CheckCircle2, UserPlus, AlertCircle } from 'lucide-react';

export default function AutoAssigner({ sprintData }) {
  const [report, setReport] = useState(null);

  useEffect(() => {
    if (sprintData?.tasks) {
      const data = sprintData.tasks.map(t => ({
        dev: t.balanced_option.devs[0] || "Unassigned",
        hours: t.balanced_option.hours
      }));
      
      const totalHours = data.reduce((sum, item) => sum + item.hours, 0);
      const devLoad = data.reduce((acc, item) => {
        acc[item.dev] = (acc[item.dev] || 0) + item.hours;
        return acc;
      }, {});

      setReport({ 
        totalHours: totalHours.toFixed(1), 
        totalTasks: data.length, 
        devLoad 
      });
    }
  }, [sprintData]);

  if (!sprintData) return null;

  return (
    <div className="mt-12 space-y-8 animate-in fade-in slide-in-from-bottom-5 duration-700">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 border-t border-slate-100 pt-12">
        
        {/* --- ASSIGNMENT LIST --- */}
        <div className="lg:col-span-2 bg-white rounded-[2.5rem] shadow-xl p-8 border border-slate-50">
          <h3 className="text-xs font-black uppercase tracking-widest text-slate-800 mb-6 flex items-center gap-2">
            <UserCheck className="text-emerald-500" size={18}/> Final Task Assignments
          </h3>
          
          <div className="space-y-3">
            {sprintData.tasks.map((task, i) => {
              const isFull = task.balanced_option.devs[0] === 'Resource Full';
              
              return (
                <div key={i} className="flex items-center justify-between p-5 bg-slate-50 rounded-2xl group hover:bg-emerald-50 transition-all border border-transparent hover:border-emerald-100">
                  <div className="flex items-center gap-4">
                    {/* Status Icon */}
                    <div className={`p-2 rounded-lg ${isFull ? 'bg-rose-100' : 'bg-emerald-100'}`}>
                      <UserPlus size={16} className={isFull ? 'text-rose-600' : 'text-emerald-600'}/>
                    </div>
                    
                    {/* Booking Info */}
                    <div className="flex flex-col">
                      <span className="text-[10px] font-black text-slate-400 uppercase tracking-tighter">
                        Confirmed Booking (Ref #{task.task_id})
                      </span>
                      <span className={`font-bold ${isFull ? 'text-rose-600' : 'text-slate-800'}`}>
                        {task.balanced_option.devs[0] || "Waiting..."}
                      </span>
                    </div>
                  </div>

                  <div className="text-right">
                    <span className="bg-white px-3 py-1 rounded-md text-[10px] font-black border border-slate-100 text-slate-900">
                      {task.balanced_option.hours}h Allocated
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* --- HEALTH REPORT --- */}
        <div className="space-y-6">
          <div className="bg-slate-900 rounded-[2.5rem] p-8 text-white shadow-2xl relative overflow-hidden">
            <FileBarChart className="absolute -right-6 -top-6 text-white/5" size={120} />
            <h3 className="text-[10px] font-black uppercase text-emerald-400 mb-8 tracking-[0.2em] flex items-center gap-2">
              <CheckCircle2 size={14}/> Sprint Health Report
            </h3>
            
            <div className="space-y-6">
              <div className="flex justify-between items-end border-b border-white/10 pb-4">
                <span className="text-slate-400 text-xs font-bold">Total Effort</span>
                <span className="text-3xl font-black">{report?.totalHours}h</span>
              </div>

              <div className="space-y-4 pt-2">
                <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Resource Distribution</p>
                {report && Object.entries(report.devLoad).map(([name, load], idx) => (
                  <div key={idx} className="space-y-2">
                    <div className="flex justify-between text-[10px] font-bold uppercase">
                      <span className={name === 'Resource Full' ? 'text-rose-400' : ''}>{name}</span>
                      <span className="text-emerald-400">{load.toFixed(1)}h</span>
                    </div>
                    <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-1000 ${name === 'Resource Full' ? 'bg-rose-500' : 'bg-emerald-500'}`} 
                        style={{ width: `${(load / report.totalHours) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="bg-amber-50 border border-amber-100 p-6 rounded-[2rem] flex items-start gap-4">
            <AlertCircle className="text-amber-600 shrink-0" size={20}/>
            <p className="text-[11px] text-amber-800 font-medium leading-relaxed">
              Assignments are optimized for <b>on-time delivery</b>. If <b>Resource Full</b> appears, consider increasing the deadline or reducing task scope.
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}