import {Link} from 'react-router-dom';
import UserOne from '../images/user/user-01.png';
import UserTwo from '../images/user/user-02.png';
import UserThree from '../images/user/user-03.png';
import UserFour from '../images/user/user-04.png';
import UserFive from '../images/user/user-05.png';


const teamMembers = [
  {
    id: 1,
    name: 'Juntao Lu',
    image: UserOne,
    job: 'Frontend Developer, Algorithm Engineer, Data Analyst',
    link: 'https://github.com/ralph0813',
    // description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In euismod ipsum et dui rhoncus auctor.',
  },
  {
    id: 2,
    name: 'Jiahao Shen',
    image: UserThree,
    job: 'Ansible Engineer, Backend Developer, Docker Engineer',
    link: '',
  },
  {
    id: 3,
    name: 'Runtian Zhang',
    image: UserFour,
    job: 'Ansible Engineer, Backend Developer, Docker Engineer',
    link: '',
  },
  {
    id: 4,
    name: 'Jie Shen',
    image: UserTwo,
    job: 'Data Analyst, UI/UX Designer',
    link: '',
  },
  {
    id: 5,
    name: 'Yuchen Liu',
    image: UserFive,
    job: 'Data Analyst, Backend Developer, Report Writer',
    link: '',
  }
]

const TeamCard = () => {
  return (
    <div
      className="col-span-12 rounded-sm border border-stroke bg-white py-6 shadow-default dark:border-strokedark dark:bg-boxdark xl:col-span-4">
      <div className="mb-6 px-7.5 text-xl font-semibold text-black dark:text-white">
        Team Members (Group 72)
      </div>

      <div>
        {teamMembers.map((member) => (
          <Link
            to={member.link}
            className="flex items-center gap-5 py-3 px-7.5 hover:bg-gray-3 dark:hover:bg-meta-4"
            key={member.id}
          >
            <div className="relative h-14 w-14 rounded-full">
              <img src={member.image} alt="avatar"/>
              {/*<span className="absolute right-0 bottom-0 h-3.5 w-3.5 rounded-full border-2 border-white bg-meta-3"></span>*/}
            </div>

            <div className="flex flex-1 items-center justify-between">
              <div>
                <div className="font-medium text-black dark:text-white">
                  {member.name}  <span className='text-sm text-body'>(Melbourne)</span>
                </div>
                <p>
                <span className="text-sm text-black dark:text-white">
                  {member.job}
                </span>
                  {/*<span className="text-xs"> . 12 min</span>*/}
                </p>
              </div>
              {/*<div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary">*/}
              {/*  <span className="text-sm font-medium text-white">3</span>*/}
              {/*</div>*/}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default TeamCard;
