using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ChatApp.ViewModel;
using System.Windows.Input;

namespace ChatApp.View.Command
{
    internal class StartClientCommand : ICommand
    {
        public event EventHandler CanExecuteChanged;
        private MainWindowViewModel parent = null;

        public StartClientCommand(MainWindowViewModel parent)
        {
            this.parent = parent;
        }

        public bool CanExecute(object parameter)
        {
            return true;
        }

        public void Execute(object parameter)
        {
            parent.startConnection();
        }
    }
}